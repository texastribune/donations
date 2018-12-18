import json
import logging
import smtplib
from collections import defaultdict
from config import (
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

from npsp import SalesforceConnection, SalesforceException


def construct_slack_message(contact=None, opportunity=None, rdo=None, account=None):
    reason = ""
    if rdo and opportunity:
        raise SalesforceException("rdo and opportunity can't both be specified")

    if account:
        amount = rdo.amount or opportunity.amount
        message = f"*{account.name}* became a business member at the *${amount}* level."
    elif opportunity:
        if opportunity.encouraged_by:
            reason = f" (encouraged by {opportunity.encouraged_by})"
        message = f"*{contact.name}* ({contact.email}) pledged *${opportunity.amount}*{reason}"
    elif rdo:
        if rdo.encouraged_by:
            reason = f" (encouraged by {rdo.encouraged_by})"
        message = f"*{contact.name}* ({contact.email}) pledged *${rdo.amount}*{reason} [{rdo.installment_period}]"

    logging.info(message)

    return message


def notify_slack(contact=None, opportunity=None, rdo=None, account=None):
    """
    Send a notification about a donation to Slack.
    """
    message = construct_slack_message(
        contact=contact, opportunity=opportunity, rdo=rdo, account=account
    )

    send_slack_message(text=message, username=opportunity.lead_source)


def send_slack_message(
    channel=SLACK_CHANNEL, text=None, username="moneybot", icon_emoji=":moneybag:"
):

    if not ENABLE_SLACK:
        return

    payload = {
        "token": SLACK_API_KEY,
        "channel": channel,
        "text": text,
        "username": username,
        "icon_emoji": icon_emoji,
    }
    url = "https://slack.com/api/chat.postMessage"
    try:
        requests.get(url, params=payload)
    except Exception as e:
        logging.error(f"Failed to send Slack notification: {e}")


def send_slack_attachment(
    channel=SLACK_CHANNEL, attachment=None, username="moneybot", icon_emoji=":moneybag:"
):
    attachment = [
        {
            "as_user": False,
            "icon_emoji": ":moneybag:",
            "fallback": "This is the fallback",
            "color": "good",
            "text": "text",
            #            "pretext": "foo@bar.com",
            "fields": [
                {"title": "Source", "value": "Amazon Alexa", "short": True},
                {"title": "Amount", "value": "$5", "short": True},
                {"title": "Name", "value": "Foo Bar", "short": False},
                {"title": "Period", "value": "yearly", "short": True},
                {"title": "Type", "value": "Circle", "short": True},
            ],
        }
    ]
    # attachment = [
    #     {
    #         "fallback": "Deployment status.",
    #         "color": "good",
    #         "mrkdwn_in": ["text"],
    #         "title": "instance_name",
    #         "fields": [
    #             {"value": "status", "short": False},
    #             {"value": "Command ID: foo", "short": False},
    #         ],
    #     }
    # ]

    from pprint import pprint

    pprint(attachment)

    if not ENABLE_SLACK:
        return
    payload = {
        "channel": channel,
        "attachments": attachment,
        "username": "Foo Bar",
        "icon_emoji": ":moneybag:",
    }
    pprint(payload)
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_API_KEY}",
        "Content-type": "application/json; charset=utf-8",
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
    except Exception as e:
        logging.error(f"Failed to send Slack notification: {e}")
    pprint(response.text, indent=2)


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
