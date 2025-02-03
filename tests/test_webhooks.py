from __future__ import absolute_import, division, print_function
import time

from flask import testing
import json
import stripe
import pytest
from werkzeug.datastructures import Headers

from server.app import app, get_contact, log_rdo, log_opportunity
from server.config import STRIPE_KEYS, STRIPE_WEBHOOK_SECRET
from server.npsp import Contact, RDO
from server.util import name_splitter

GOOD_WEBHOOK_PAYLOAD = {
    "id": "evt_test_webhook",
    "type": "evt_wingus",
    "data": {
        "object": {},
    },
}

BAD_WEBHOOK_PAYLOAD = {
    "id": "evt_test_webhook",
    "type": "evt_wingus",
}

MOCK_SUB_OBJ = {
    "customer": "cus_NskMDwAXZUuQFZ",
}

@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": ["authorization"],
        "ignore_localhost": True,
        "record_mode": "once",
    }

def generate_header(**kwargs) -> str:
    timestamp = kwargs.get("timestamp", int(time.time()))
    payload = kwargs.get("payload", json.dumps(GOOD_WEBHOOK_PAYLOAD))
    secret = kwargs.get("secret", STRIPE_WEBHOOK_SECRET)
    scheme = kwargs.get("scheme", stripe.WebhookSignature.EXPECTED_SCHEME)
    signature = kwargs.get("signature", None)
    if signature is None:
        payload_to_sign = "%d.%s" % (timestamp, payload)
        signature = stripe.WebhookSignature._compute_signature(
            payload_to_sign, secret
        )
    header = "t=%d,%s=%s" % (timestamp, scheme, signature)
    return header

def mock_contact_get_or_create(email, first_name=None, last_name=None, zipcode=None, id=None):
    print("Creating contact...")
    contact = Contact()
    contact.id = id
    contact.email = email
    contact.first_name = first_name
    contact.last_name = last_name
    contact.mailing_postal_code = zipcode
    return contact

def mock_rdo_save(self):
    pass

def mock_opportunity_save(self):
    pass


class WebhookTestClient(testing.FlaskClient):
    def open(self, *args, **kwargs):
        new_headers = Headers({'Stripe-Signature': generate_header()})
        headers = kwargs.pop('headers', Headers())
        headers.extend(new_headers)
        kwargs['headers'] = headers
        return super().open(*args, **kwargs)

@pytest.fixture
def client():
    app.test_client_class = WebhookTestClient
    return app.test_client()

def test_stripehook_good_sig(client):
    response = client.post('/stripehook', data=json.dumps(GOOD_WEBHOOK_PAYLOAD))
    assert response.status_code==200

def test_stripehook_bad_sig(client):
    response = client.post('/stripehook', data=json.dumps(BAD_WEBHOOK_PAYLOAD))
    assert response.status_code==400

# TODO: ask Anna about better ways to mock/record/test Salesforce
# vcr records the request to the stripe api, and keeps the results for reuse
@pytest.mark.vcr
def test_get_contact(mocker):
    mocker.patch(
        'server.app.Contact.get_or_create',
        mock_contact_get_or_create
    )
    customer = stripe.Customer.retrieve("cus_O2nNxZMg42Z8e3")
    resp = get_contact(customer)
    assert resp.email=='matthew.d.mccrary@gmail.com'
    assert resp.first_name=='Matthew'
    assert resp.last_name=='Dylan'
    assert resp.mailing_postal_code=='78735'

@pytest.mark.vcr
def test_log_rdo(mocker):
    mocker.patch(
        'server.app.RDO.save',
        mock_rdo_save,
    )

    subscription = stripe.Subscription.retrieve("sub_1N6yrwCUjA8cLeTjW4JOOjwx")
    contact = Contact()
    contact.id = "0031700000BHQzBAAX"
    contact.email = "thenils.testing.account@proton.me"
    contact.first_name = "Harry"
    contact.last_name = "Nilsson"

    resp = log_rdo(type="membership", contact=contact, subscription=subscription)
    assert resp.stripe_customer=="cus_NskMDwAXZUuQFZ"
    assert resp.campaign_id=="limeinthecoconut123456789"
    assert resp.referral_id=="puppysong123456789"
    assert resp.agreed_to_pay_fees==True
    assert resp.encouraged_by=="Let the good times roll"
    assert resp.amount=="0.00"
    assert resp.installment_period=="monthly"
    assert resp.quarantined==False
    assert resp.stripe_card_expiration=="2024-02-29"
    assert resp.stripe_card_brand=="MasterCard"
    assert resp.stripe_card_last_4=="4444"

@pytest.mark.vcr
def test_log_opportunity(mocker):
    mocker.patch(
        'server.app.Opportunity.save',
        mock_opportunity_save,
    )

    payment_intent = stripe.PaymentIntent.retrieve("pi_3NGhmhCUjA8cLeTj1bBvkJ1o")
    contact = Contact()
    contact.id = "0031700000BHQzBAAX"
    contact.email = "thenils.testing.account@proton.me"
    contact.first_name = "Harry"
    contact.last_name = "Nilsson"

    resp = log_opportunity(contact, payment_intent)

    assert resp.stripe_customer=="cus_O2nNxZMg42Z8e3"
    assert resp.amount=="20.00"
    assert resp.stripe_card_expiration=="2024-04-30"
    assert resp.stripe_card_brand=="Visa"
    assert resp.stripe_card_last_4=="4242"

def test_name_splitter():
    first_name, last_name = name_splitter('Harry Nilsson')
    assert first_name=='Harry'
    assert last_name=='Nilsson'
