import logging
from config import ACCOUNTING_MAIL_RECIPIENT, LOG_LEVEL, REDIS_URL, TIMEZONE
from datetime import datetime, timedelta

from pytz import timezone

import redis
from celery import shared_task
from charges import amount_to_charge, charge, ChargeException
from npsp import Opportunity
from util import send_email

zone = timezone(TIMEZONE)


log_level = logging.getLevelName(LOG_LEVEL)

root = logging.getLogger()
root.setLevel(log_level)


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
        logging.debug(string)
        self.log.append(string)

    def send(self):
        """
        Send the assembled log out as an email.
        """
        body = "\n".join(self.log)
        recipient = ACCOUNTING_MAIL_RECIPIENT
        subject = "Batch run"
        send_email(body=body, recipient=recipient, subject=subject)


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


# TODO stop sending this email and just rely on Sentry and logs?


@shared_task()
def charge_cards():

    lock = Lock(key="charge-cards-lock")
    lock.acquire()

    log = Log()

    log.it("---Starting batch job...")

    three_days_ago = (datetime.now(tz=zone) - timedelta(days=10)).strftime("%Y-%m-%d")
    today = datetime.now(tz=zone).strftime("%Y-%m-%d")

    opportunities = Opportunity.list(begin=three_days_ago, end=today)

    log.it("---Processing charges...")

    log.it(f"Found {len(opportunities)} opportunities available to process.")

    for opportunity in opportunities:
        if not opportunity.stripe_customer:
            continue
        amount = amount_to_charge(opportunity)
        log.it(
            f"---- Charging ${amount} to {opportunity.stripe_customer} ({opportunity.name})"
        )
        try:
            charge(opportunity)
        except ChargeException as e:
            logging.info("Batch charge error")
            e.send_slack_notification()

    log.send()

    lock.release()


if __name__ == "__main__":
    charge_cards()
