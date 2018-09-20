from datetime import datetime
from decimal import Decimal
import locale

import celery
import requests
from pytz import timezone

from config import TIMEZONE
from config import ENABLE_SLACK
from config import SLACK_API_KEY
from config import SLACK_CHANNEL
from config import MULTIPLE_ACCOUNT_WARNING_MAIL_RECIPIENT

from emails import send_email
from sf import Contact, Opportunity, RDO
from util import clean

zone = timezone(TIMEZONE)

locale.setlocale(locale.LC_ALL, "C")

TWOPLACES = Decimal(10) ** -2  # same as Decimal('0.01')


def notify_slack(contact=None, opportunity=None, rdo=None):
    """
    Send a notification about a donation to Slack.
    """
    reason = ""
    if opportunity:
        if opportunity.encouraged_by:
            reason = f" (encouraged by {opportunity.encouraged_by})"
        message = f"*{contact.name}* ({contact.email}) pledged *${opportunity.amount}*{reason}"

    if rdo:
        if rdo.encouraged_by:
            reason = f" (encouraged by {rdo.encouraged_by})"
        message = f"*{contact.name}* ({contact.email}) pledged *${rdo.amount}*{reason} [{rdo.installment_period}]"

    if not ENABLE_SLACK:
        print(message)
        return

    payload = {
        "token": SLACK_API_KEY,
        "channel": SLACK_CHANNEL,
        "text": message,
        "username": "moneybot",
        "icon_emoji": ":moneybag:",
    }
    url = "https://slack.com/api/chat.postMessage"
    try:
        requests.get(url, params=payload)
    except Exception as e:
        print("Failed to send Slack notification: {}".format(e))


def send_multiple_account_warning(contact):
    """
    Send the warnings about multiple accounts.
    """

    body = f"""
    Multiple accounts were found matching the email address <{contact.email}>
    while inserting a transaction.

    The transaction was attached to the first match found. You may want to
    move the transaction to the proper account if the one chosen is not
    correct. You may also want to delete or otherwise correct the duplicate
    account(s).
    """

    send_email(
        recipient=MULTIPLE_ACCOUNT_WARNING_MAIL_RECIPIENT,
        subject=f"Multiple accounts found for {contact.email}",
        body=body,
    )


def get_email(form):
    if "subscriber_email" in form:
        email = form["subscriber_email"]
        print("found subscriber email: {}".format(email))
        return email
    else:
        return form.get("stripeEmail")


def _format_contact(form=None):
    """
    Format a contact for update/insert.
    """

    email = get_email(form)

    stripe_id = form.get("Stripe_Customer_Id__c", None)

    zipcode = form.get("zipcode", None)

    contact = {
        "Email": email,
        "FirstName": form["first_name"],
        "LastName": form["last_name"],
        "Description": form["description"],
        "LeadSource": "Stripe",
        "Stripe_Customer_Id__c": stripe_id,
        "MailingPostalCode": zipcode,
    }
    print(contact)
    return contact


def add_opportunity(contact=None, form=None, customer=None):

    print("----Adding opportunity...")

    opportunity = Opportunity(contact=contact)
    opportunity.amount = form.get("amount", 0)
    opportunity.stripe_customer = customer["id"]
    opportunity.campaign_id = form["campaign_id"]
    opportunity.referral_id = form["referral_id"]
    opportunity.description = "Texas Tribune Membership"
    opportunity.agreed_to_pay_fees = form["pay_fees_value"]
    opportunity.encouraged_by = form["reason"]
    opportunity.lead_source = "Stripe"

    opportunity.save()
    return opportunity


def add_recurring_donation(contact=None, form=None, customer=None):

    if form["installment_period"] is None:
        raise Exception("installment_period must have a value")

    rdo = RDO(contact=contact)

    rdo.stripe_customer = customer["id"]
    rdo.campaign_id = form["campaign_id"]
    rdo.referral_id = form["referral_id"]
    rdo.description = "Texas Tribune Sustaining Membership"
    rdo.agreed_to_pay_fees = form["pay_fees_value"]
    rdo.encouraged_by = form["reason"]
    rdo.lead_source = "Stripe"
    rdo.amount = form.get("amount", 0)

    installments = form["installments"]

    open_ended_status = form["openended_status"]
    installment_period = form["installment_period"]
    rdo.open_ended_status = open_ended_status
    rdo.installments = installments
    rdo.installment_period = installment_period

    if (
        open_ended_status is None
        and (installments == 3 or installments == 36)
        and (installment_period == "yearly" or installment_period == "monthly")
    ):
        rdo.type = "Giving Circle"
        rdo.description = "Texas Tribune Circle Membership"

    rdo.save()

    return rdo


@celery.task(name="salesforce.add_donation")
def add_donation(form=None, customer=None):
    """
    Add a contact and their donation into SF. This is done in the background
    because there are a lot of API calls and there's no point in making the
    payer wait for them.
    """
    form = clean(form)
    first_name = form["first_name"]
    last_name = form["last_name"]
    period = form["installment_period"]
    email = form["stripeEmail"]
    zipcode = form["zipcode"]

    print("----Getting contact....")
    contact = Contact.get_or_create(
        email=email, first_name=first_name, last_name=last_name, zipcode=zipcode
    )

    # intentionally overwriting zip but not name here

    if not contact.created:
        contact.zipcode = zipcode
        contact.save()

    if period is None:
        print("----Creating one time payment...")
        opportunity = add_opportunity(contact=contact, form=form, customer=customer)
        notify_slack(contact=contact, opportunity=opportunity)
    else:
        print("----Creating recurring payment...")
        rdo = add_recurring_donation(contact=contact, form=form, customer=customer)
        notify_slack(contact=contact, rdo=rdo)

    if contact.duplicate_found:
        send_multiple_account_warning(contact)

    return True


@celery.task(name="salesforce.add_blast_subcription")
def add_blast_subscription(form=None, customer=None):

    form = clean(form)

    first_name = form["first_name"]
    last_name = form["last_name"]
    email = form["subscriber_email"]

    print("----Getting contact...")
    contact = Contact.get_or_create(
        email=email, first_name=first_name, last_name=last_name
    )

    rdo = RDO(contact=contact)

    rdo.stripe_customer = customer["id"]
    rdo.campaign_id = form["campaign_id"]
    rdo.referral_id = form["referral_id"]
    rdo.lead_source = "Stripe"
    rdo.amount = form.get("amount", 0)
    rdo.agreed_to_pay_fees = form["pay_fees_value"]

    # Blast specific:
    rdo.installments = 0
    rdo.description = "Blast Subscription"
    rdo.open_ended_status = "Open"
    if rdo.amount == 40:
        rdo.installment_period = "monthly"
    else:
        rdo.installment_period = "yearly"
    now = datetime.now(tz=zone).strftime("%Y-%m-%d %I:%M:%S %p %Z")
    rdo.name = f"{first_name} {last_name} - {now} - The Blast"
    rdo.type = "The Blast"
    rdo.billing_email = form["stripeEmail"]
    rdo.blast_subscription_email = form["subscriber_email"]

    print("----Saving RDO....")
    rdo.save()

    return True
