import email
import email.policy
import smtplib

import pytest

from server import batch, util
from server.npsp import Contact


class FakeSMTP(smtplib.SMTP):
    """
    smtplib.SMTP with the network calls stubbed out. sendmail() and
    send_message() still run for real, so any encoding error they raise
    surfaces here just like it would against a real mail server.
    """

    sent = []

    def __init__(self, *args, **kwargs):
        super().__init__()

    def ehlo(self, *args, **kwargs):
        self.ehlo_resp = b"fake"
        self.esmtp_features = {}
        return 250, b"ok"

    def starttls(self, *args, **kwargs):
        return 220, b"ok"

    def login(self, *args, **kwargs):
        return 235, b"ok"

    def mail(self, *args, **kwargs):
        return 250, b"ok"

    def rcpt(self, *args, **kwargs):
        return 250, b"ok"

    def data(self, msg):
        FakeSMTP.sent.append(msg)
        return 250, b"ok"

    def close(self):
        pass


@pytest.fixture
def outbox(monkeypatch):
    FakeSMTP.sent = []
    monkeypatch.setattr(util.smtplib, "SMTP", FakeSMTP)
    return FakeSMTP.sent


def parse(raw):
    return email.message_from_bytes(raw, policy=email.policy.default)


def test_send_email_sets_headers(outbox):
    util.send_email(
        recipient=["accounting", "revenue"],
        subject="Batch run",
        body="All charges succeeded",
        sender="donations",
    )

    assert len(outbox) == 1
    message = parse(outbox[0])
    assert message["From"] == "donations"
    assert message["To"] == "accounting, revenue"
    assert message["Subject"] == "Batch run"
    assert message.get_content().strip() == "All charges succeeded"


def test_send_email_keeps_non_ascii_body(outbox):
    util.send_email(
        recipient="accounting",
        subject="New business membership",
        body="A new business membership has been received for Café Olé:\n\nJosé Peña",
        sender="donations",
    )

    assert len(outbox) == 1
    body = parse(outbox[0]).get_content()
    assert "Café Olé" in body
    assert "José Peña" in body


def test_send_email_with_non_ascii_subject(outbox):
    util.send_email(
        recipient="accounting",
        subject="Multiple accounts found for josé",
        body="body",
        sender="donations",
    )

    assert len(outbox) == 1
    assert parse(outbox[0])["Subject"] == "Multiple accounts found for josé"


def test_send_email_defaults_sender(outbox, monkeypatch):
    monkeypatch.setattr(util, "DEFAULT_MAIL_SENDER", "default-sender")
    util.send_email(recipient="accounting", subject="Batch run", body="body")

    assert parse(outbox[0])["From"] == "default-sender"


def test_batch_log_send_with_accented_names(outbox, monkeypatch):
    monkeypatch.setattr(batch, "ACCOUNTING_MAIL_RECIPIENT", "accounting")
    log = batch.Log()
    log.it("---Processing charges...")
    log.it("---- Charging $10.00 to José Peña (Renée Côté)")
    log.send()

    assert len(outbox) == 1
    message = parse(outbox[0])
    assert message["Subject"] == "Batch run"
    assert "José Peña (Renée Côté)" in message.get_content()


def test_multiple_account_warning_with_non_ascii_address(outbox, monkeypatch):
    monkeypatch.setattr(util, "MULTIPLE_ACCOUNT_WARNING_MAIL_RECIPIENT", "accounting")
    contact = Contact()
    contact.email = "josé.peña"
    util.send_multiple_account_warning(contact)

    assert len(outbox) == 1
    message = parse(outbox[0])
    assert message["Subject"] == "Multiple accounts found for josé.peña"
    assert "<josé.peña>" in message.get_content()


def test_send_email_logs_instead_of_raising_on_bad_header(outbox, caplog):
    util.send_email(
        recipient="accounting",
        subject="Batch run\nBcc: someone-else",
        body="body",
        sender="donations",
    )

    assert outbox == []
    assert "failed to send mail" in caplog.text
