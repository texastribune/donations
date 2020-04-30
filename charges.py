import calendar
import logging
from decimal import Decimal
from config import STRIPE_KEYS, CIRCLE_FAILURE_RECIPIENT
from npsp import User, Task
from util import send_slack_message

import stripe

stripe.api_key = STRIPE_KEYS["secret_key"]

TWOPLACES = Decimal(10) ** -2  # same as Decimal('0.01')


class ChargeException(Exception):
    def __init__(self, opportunity, message):
        super().__init__(message)
        self.opportunity = opportunity
        self.message = message

    def send_slack_notification(self):
        send_slack_message(
            {
                "channel": "#stripe",
                "text": f"Charge failed for {self.opportunity.name} [{self.message}]",
                "icon_emoji": ":x:",
            }
        )


def amount_to_charge(opportunity):
    """
    Determine the amount to charge. This depends on whether the payer agreed
    to pay fees or not. If they did then we add that to the amount charged.
    Stripe charges 2.2% + $0.30.

    https://support.stripe.com/questions/can-i-charge-my-stripe-fees-to-my-customers
    """
    amount = float(opportunity.amount)
    if opportunity.agreed_to_pay_fees:
        total = (amount + 0.30) / (1 - 0.022)
    else:
        total = amount
    return quantize(total)


def quantize(amount):
    return Decimal(amount).quantize(TWOPLACES)


def charge(opportunity):

    amount = amount_to_charge(opportunity)
    logging.info(
        f"---- Charging ${amount} to {opportunity.stripe_customer} ({opportunity.name})"
    )
    if opportunity.stage_name != "Pledged":
        raise Exception(f"Opportunity {opportunity.id} is not Pledged")

    opportunity.stage_name = "In Process"
    opportunity.save()

    try:
        card_charge = stripe.Charge.create(
            customer=opportunity.stripe_customer,
            amount=int(amount * 100),
            currency="usd",
            description=opportunity.description,
            metadata={
                "opportunity_id": opportunity.id,
                "account_id": opportunity.account_id,
            },
        )
    except stripe.error.CardError as e:
        # look for decline code:
        error = e.json_body["error"]
        logging.info(f"The card has been declined:")
        logging.info(f"Message: {error.get('message', '')}")
        logging.info(f"Decline code: {error.get('decline_code', '')}")
        opportunity.closed_lost_reason = error.get("message", "unknown failure")
        opportunity.stage_name = "Closed Lost"
        opportunity.save()
        logging.debug(
            f"Opportunity set to '{opportunity.stage_name}' with reason: {opportunity.closed_lost_reason}"
        )
        if opportunity.type == "Giving Circle":
            user = User.get(CIRCLE_FAILURE_RECIPIENT)
            subject = "Credit card charge failed for Circle member"
            task = Task(owner_id=user.id, what_id=opportunity.id, subject=subject)
            task.save()
            send_slack_message(
                {
                    "channel": "#circle-failures",
                    "text": f"Circle charge failed for {opportunity.name} [{opportunity.closed_lost_reason}]",
                    "icon_emoji": ":x:",
                }
            )

        raise ChargeException(opportunity, "card error")

    except stripe.error.InvalidRequestError as e:
        logging.error(f"Problem: {e}")
        raise ChargeException(opportunity, "invalid request")
    except Exception as e:
        logging.error(f"Problem: {e}")
        raise ChargeException(opportunity, "unknown error")

    if card_charge.status != "succeeded":
        logging.error("Charge failed. Check Stripe logs.")
        raise ChargeException(opportunity, "charge failed")

    # There's a lot going on here. Up to this point the donor selected an
    # amount (say $100) and decided if they wanted to pay our processing
    # fees. We recorded those two bits of information in the opportunity or the
    # RDO. Now we're actually charging the card so we have new information:
    # what the actual processing fees. So we we move stuff around. The
    # original amount the donor selected was stored in the "amount" field of
    # the opportunity or the RDO. That amount gets moved to "donor selected
    # amount" on the opportunity. Now the amount field on the opportunity will
    # represeent the gross amount (the point of this whole thing) and the
    # amount minus processing fees gets stored on the opportunity field in "net
    # amount". We didn't know that amount up until the charge took place
    # because Amex.
    balance_transaction = stripe.BalanceTransaction.retrieve(
        card_charge.balance_transaction
    )
    opportunity.donor_selected_amount = opportunity.amount
    opportunity.net_amount = balance_transaction.net / 100
    opportunity.amount = amount  # gross
    gross = card_charge.amount / 100

    opportunity.stripe_card = card_charge.source.id
    opportunity.stripe_transaction_id = card_charge.id
    opportunity.stage_name = "Closed Won"
    opportunity.save()
