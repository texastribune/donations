from collections import defaultdict
import smtplib

import requests

from config import MAIL_SERVER
from config import MAIL_PORT
from config import MAIL_USERNAME
from config import MAIL_PASSWORD
from config import DEFAULT_MAIL_SENDER
from config import ENABLE_SLACK
from config import SLACK_API_KEY
from config import SLACK_CHANNEL
from config import MULTIPLE_ACCOUNT_WARNING_MAIL_RECIPIENT


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


def clean(form=None):
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
        print("successfully sent the mail")
    except Exception as e:
        print("failed to send mail: {}".format(e))
