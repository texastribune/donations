import logging
from decimal import Decimal

import stripe

from .config import CIRCLE_FAILURE_RECIPIENT, STRIPE_KEYS
from .npsp import Task, User
from .util import send_slack_message

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


class QuarantinedException(Exception):
    pass


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


def generate_stripe_description(opportunity) -> str:
    """
    Our current code populates the Description field of recurring donations
    and opportunities when those are created. Those descriptions get passed
    on to Stripe when the card is charged. But we have at least two cases
    where the Description field could be blank: when someone manually enters
    a donation or when it's a donation that's been migrated from our legacy
    (Tinypass) system. But in those cases we know the opportunity type and
    it's a direct relationship to the description so we can populate it anyway.
    """
    # remove leading "The " from descriptions for better Stripe
    if opportunity.description:
        if opportunity.description.startswith("The "):
            return opportunity.description[4:]
        else:
            return opportunity.description

    description_map = {
        "The Blast": "Blast Subscription",
        "Recurring Donation": "Texas Tribune Sustaining Membership",
        "Single": "Texas Tribune Membership",
        "Giving Circle": "Texas Tribune Circle Membership",
    }
    if opportunity.type in description_map.keys():
        return description_map[opportunity.type]
    else:
        return "Texas Tribune"


def charge(opportunity):

    amount = amount_to_charge(opportunity)
    logging.info(
        f"---- Charging ${amount} to {opportunity.stripe_customer} ({opportunity.name})"
    )
    if opportunity.stage_name != "Pledged":
        raise Exception(f"Opportunity {opportunity.id} is not Pledged")
    if opportunity.quarantined:
        logging.info("---- Skipping because it's quarantined")
        raise QuarantinedException(f"Opportunity {opportunity.id} is quarantined")

    opportunity.stage_name = "In Process"
    opportunity.save()

    try:
        card_charge = stripe.Charge.create(
            customer=opportunity.stripe_customer,
            amount=int(amount * 100),
            currency="usd",
            description=generate_stripe_description(opportunity),
            metadata={
                "opportunity_id": opportunity.id,
                "account_id": opportunity.account_id,
            },
        )
    except Exception as e:
        logging.info(f"Error charging card: {type(e)}")
        if isinstance(e, stripe.error.StripeError):
            message = e.user_message or ""
            logging.info(f"Message: {message}")

            reason = e.user_message

            if isinstance(e, stripe.error.CardError):
                logging.info("The card has been declined")
                logging.info(f"Decline code: {e.json_body.get('decline_code', '')}")

                if reason is None:
                    reason = "card declined for unknown reason"

            if reason is None:
                reason = "unknown failure"
        else:
            reason = "unknown failure"

        opportunity.closed_lost_reason = reason
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

        raise ChargeException(opportunity, reason)

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
