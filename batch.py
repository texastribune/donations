import logging
from config import ACCOUNTING_MAIL_RECIPIENT, REDIS_URL, STRIPE_KEYS, TIMEZONE
from datetime import datetime, timedelta
from decimal import Decimal

from pytz import timezone

import celery
import redis
import stripe
from npsp import Opportunity
from util import send_email

zone = timezone(TIMEZONE)

stripe.api_key = STRIPE_KEYS["secret_key"]

TWOPLACES = Decimal(10) ** -2  # same as Decimal('0.01')


def quantize(amount):
    return Decimal(amount).quantize(TWOPLACES)


class Log(object):
    """
    This encapulates sending to the console/stdout and email all in one.

    """

    def __init__(self):
        self.log = list()

    def it(self, string):
        """
        Add something to the log.
        """
        logging.info(string)
        self.log.append(string)

    def send(self):
        """
        Send the assembled log out as an email.
        """
        body = "\n".join(self.log)
        recipient = ACCOUNTING_MAIL_RECIPIENT
        subject = "Batch run"
        send_email(body=body, recipient=recipient, subject=subject)


def amount_to_charge(amount, pay_fees=False):
    """
    Determine the amount to charge. This depends on whether the payer agreed
    to pay fees or not. If they did then we add that to the amount charged.
    Stripe charges 2.2% + $0.30.

    https://support.stripe.com/questions/can-i-charge-my-stripe-fees-to-my-customers
    """
    amount = float(amount)
    if pay_fees:
        total = (amount + .30) / (1 - 0.022)
    else:
        total = amount
    return quantize(total)


class AlreadyExecuting(Exception):
    """
    Here to show when more than one job of the same type is running.
    """

    pass


class Lock(object):
    """
    Claim an exclusive lock. Using Redis.
    """

    def __init__(self, key):
        self.key = key
        self.connection = redis.from_url(REDIS_URL)

    def acquire(self):
        if self.connection.get(self.key):
            raise AlreadyExecuting
        self.connection.setex(name=self.key, value="bar", time=1200)

    def release(self):
        self.connection.delete(self.key)


@celery.task()
def charge_cards():

    lock = Lock(key="charge-cards-lock")
    lock.acquire()

    log = Log()

    log.it("---Starting batch job...")

    three_days_ago = (datetime.now(tz=zone) - timedelta(days=3)).strftime("%Y-%m-%d")
    today = datetime.now(tz=zone).strftime("%Y-%m-%d")

    opportunities = Opportunity.list_pledged(begin=three_days_ago, end=today)

    log.it("---Processing charges...")

    log.it(f"Found {len(opportunities)} opportunities available to process.")

    for item in opportunities:
        if not item.stripe_customer:
            continue
        amount = amount_to_charge(amount=item.amount, pay_fees=item.agreed_to_pay_fees)
        try:
            log.it(f"---- Charging ${amount} to {item.stripe_customer} ({item.name})")

            charge = stripe.Charge.create(
                customer=item.stripe_customer,
                amount=int(amount * 100),
                currency="usd",
                description=item.description,
            )
        except stripe.error.CardError as e:
            # look for decline code:
            error = e.json_body["error"]
            log.it("The card has been declined:")
            log.it("\tStatus: {}".format(e.http_status))
            log.it("\tType: {}".format(error.get("type", "")))
            log.it("\tCode: {}".format(error.get("code", "")))
            log.it("\tParam: {}".format(error.get("param", "")))
            log.it("\tMessage: {}".format(error.get("message", "")))
            log.it("\tDecline code: {}".format(error.get("decline_code", "")))
            continue
        except stripe.error.InvalidRequestError as e:
            log.it("Problem: {}".format(e))
            continue
        except Exception as e:
            log.it("Problem: {}".format(e))
            continue
        if charge.status != "succeeded":
            log.it("Charge failed. Check Stripe logs.")
            continue
        item.stripe_transaction_id = charge.id
        item.stripe_card = charge.source.id
        item.stage_name = "Closed Won"
        item.save()
        log.it("ok")

    log.send()

    lock.release()


if __name__ == "__main__":
    charge_cards()
