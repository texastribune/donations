import calendar
import logging
from decimal import Decimal
from config import STRIPE_KEYS, CIRCLE_FAILURE_RECIPIENT
from npsp import User, Task
from util import send_slack_message

import stripe

stripe.api_key = STRIPE_KEYS["secret_key"]

TWOPLACES = Decimal(10) ** -2  # same as Decimal('0.01')


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
        return

    except stripe.error.InvalidRequestError as e:
        logging.error(f"Problem: {e}")
        # TODO should we raise this?
        return
    except Exception as e:
        logging.error(f"Problem: {e}")
        # TODO should we raise this?
        return

    if card_charge.status != "succeeded":
        logging.error("Charge failed. Check Stripe logs.")
        # TODO should we raise this?
        return

    opportunity.stripe_card = card_charge.source.id
    opportunity.stripe_transaction_id = card_charge.id
    opportunity.stage_name = "Closed Won"
    opportunity.save()
