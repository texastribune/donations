import json
import hashlib
import logging
import smtplib
from collections import defaultdict
from .config import (
    BUSINESS_MEMBER_RECIPIENT,
    DEFAULT_MAIL_SENDER,
    ENABLE_SLACK,
    MAIL_PASSWORD,
    MAIL_PORT,
    MAIL_SERVER,
    MAIL_USERNAME,
    MULTIPLE_ACCOUNT_WARNING_MAIL_RECIPIENT,
    SLACK_API_KEY,
    SLACK_CHANNEL,
)

import requests

from .npsp import SalesforceConnection, SalesforceException, DEFAULT_RDO_TYPE


def construct_slack_message(contact=None, opportunity=None, rdo=None, account=None):

    if rdo and opportunity:
        raise SalesforceException("rdo and opportunity can't both be specified")

    opp = opportunity or rdo

    entity = account.name if account else contact.name

    amount = getattr(opp, "amount", False) or ""
    amount = float(amount)

    period = f"[{rdo.installment_period}]" if rdo else "[one-time]"

    reason = getattr(opp, "encouraged_by", False) or ""
    reason = f"({reason})" if reason else ""

    campaign = getattr(opp, "campaign_name", False) or ""
    campaign = f"({campaign})" if campaign else ""

    message = f"{entity} pledged ${amount:.0f} {period} {reason} {campaign}"

    logging.info(message)

    return message


def notify_slack(contact=None, opportunity=None, rdo=None, account=None):
    """
    Send a notification about a donation to Slack.
    """

    opp = opportunity or rdo
    if opp.campaign_id:
        opp.campaign_name = opp.get_campaign_name()

    text = construct_slack_message(
        contact=contact, opportunity=opportunity, rdo=rdo, account=account
    )
    username = rdo.lead_source if rdo else opportunity.lead_source
    message = {"text": text, "channel": SLACK_CHANNEL, "icon_emoji": ":moneybag:"}

    send_slack_message(message, username=username)


def send_slack_message(message=None, username="moneybot"):

    if not ENABLE_SLACK or not message:
        return
    message["token"] = SLACK_API_KEY
    message["username"] = username
    url = "https://slack.com/api/chat.postMessage"
    try:
        response = requests.post(url, params=message)
        slack_response = json.loads(response.text)
        if not slack_response["ok"]:
            raise Exception(slack_response["error"])
    except Exception as e:
        logging.error(f"Failed to send Slack notification: {e}")


def construct_slack_attachment(
    email=None,
    donor=None,
    source=None,
    amount=None,
    period=None,
    donation_type=None,
    reason=None,
):
    """
    Not currently in use.
    """

    grav_hash = hashlib.md5(email.lower().encode("utf-8")).hexdigest()

    attachment = {
        "fallback": "Donation",
        "color": "good",
        # "pretext": "optional and appears above attachment"
        # # "text": "text",
        "author_name": donor,
        # author_link
        "author_icon": f"https://www.gravatar.com/avatar/{grav_hash}?s=16&r=g&default=robohash",
        "title": email,
        # "title_link":
        # "text": reason,
        # title_link
        "fields": [
            {"title": "Source", "value": source, "short": True},
            {"title": "Amount", "value": f"${amount}", "short": True},
            {"title": "Period", "value": period, "short": True},
            {"title": "Type", "value": donation_type, "short": True},
        ],
        # "image_url":
        # "thumb_url":
        # "footer":
        # "footer_icon":
        # "ts":
    }
    if reason:
        attachment["text"] = reason

    return attachment


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


def clean(form):
    """
    Clean up a form by converting strings to their 'None' or boolean equivalents and converting string numbers to their native types. Also makes None the response if the form is asked for a missing key.
    """
    result = defaultdict(lambda: None)
    for k, v in form.items():
        if v is None or v == "None":
            result[k] = None
            continue
        if v is True or v == "True":
            result[k] = True
            continue
        if v is False or v == "False":
            result[k] = False
            continue
        if isinstance(v, (int, float)):
            result[k] = v
            continue
        try:
            result[k] = int(v)
            continue
        except ValueError:
            try:
                result[k] = float(v)
                continue
            except ValueError:
                result[k] = v
    return result


def send_email(recipient, subject, body, sender=None):

    if sender is None:
        FROM = DEFAULT_MAIL_SENDER
    else:
        FROM = sender

    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (
        FROM,
        ", ".join(TO),
        SUBJECT,
        TEXT,
    )
    try:
        server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        server.ehlo()
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.sendmail(FROM, TO, message)
        server.close()
        logging.debug("successfully sent the mail")
    except Exception as e:
        logging.error(f"failed to send mail: {e}")


def send_email_new_business_membership(account, contact):

    if not BUSINESS_MEMBER_RECIPIENT:
        raise Exception("BUSINESS_MEMBER_RECIPIENT must be specified")

    url = SalesforceConnection().instance_url

    body = f"A new business membership has been received for {account.name}:\n\n"

    body += f"{url}/{account.id}\n\n"
    if account.created:
        body += "A new account was created.\n\n"

    body += f"It was created by {contact.name}:\n\n"

    body += f"{url}/{contact.id}\n\n"

    if contact.created:
        body += "A new contact was created."

    logging.info(body)
    send_email(
        recipient=BUSINESS_MEMBER_RECIPIENT,
        subject="New business membership",
        body=body,
    )


def name_splitter(name) -> tuple:
    name_array = name.split(" ", 1) if name else ["", ""]
    return name_array[0], name_array[1]
