from datetime import datetime
import logging
import vcr
from decimal import Decimal
from unittest.mock import patch

from pytz import timezone

import pytest
from batch import amount_to_charge
from npsp import (
    RDO,
    Contact,
    Opportunity,
    SalesforceConnection,
    SalesforceObject,
    Account,
)
from util import clean, construct_slack_message

vcr = vcr.VCR(
    cassette_library_dir="fixtures/cassettes",
    record_mode="once",
    filter_headers=["authorization", "cookie"],
    decode_compressed_response=True,
    path_transformer=vcr.VCR.ensure_suffix(".yaml"),
)
# import ptvsd
#
# ptvsd.enable_attach()
# ptvsd.wait_for_attach()


class SalesforceConnectionSubClass(SalesforceConnection):
    def __init__(self):
        pass


sf = SalesforceConnectionSubClass()

from pprint import pprint

vcr_log = logging.getLogger("vcr")
vcr_log.setLevel(logging.WARNING)


# @vcr.use_cassette
def test_serialize_object_has_id():
    opp = Opportunity()
    opp.id = "006S000000DrUps"
    opp.amount = 5
    breakpoint()
    result = opp.serialize()
    # TODO: result['Amount'] is $213.04 -- the amount that's in the opp in SF; presumably because I hadn't save()d it yet;
    # what should be the behavior?
    # TODO should serialize() be _private?
    # TODO: what to do about RecordType.Name?
    assert "created" not in result
    assert "duplicate_found" not in result
    assert len(result) == 2  # 'Amount' and 'RecordType.Name'
    assert result["Amount"] == 5


@vcr.use_cassette
def test_serialize():
    opp = Opportunity()
    opp.amount = 5
    result = opp.serialize()
    assert result["Amount"] == 5


def test_setattr():
    obj = Opportunity()
    obj.foo = "bar"
    assert obj.tainted == set()
    obj.foo = "baz"
    assert "foo" in obj.tainted
    assert len(obj.tainted) == 1


def test__clean():
    form = {
        "a": "None",
        "b": "True",
        "c": "False",
        "d": "None",
        "e": "none",
        "f": None,
        "g": True,
        "h": False,
        "i": 9,
        "j": 8.1,
        "k": "3.2",
        "l": "4",
        "m": "string",
    }
    expected = {
        "a": None,
        "b": True,
        "c": False,
        "d": None,
        "e": "none",
        "f": None,
        "g": True,
        "h": False,
        "i": 9,
        "j": 8.1,
        "k": 3.2,
        "l": 4,
        "m": "string",
    }
    actual = clean(form)
    assert expected == actual
    assert actual["bogus"] is None


class Response(object):
    pass


@vcr.use_cassette
def test_get_schema():

    Opportunity.get_schema()
    assert Opportunity.attr_to_field_map
    assert Opportunity.field_to_attr_map


def test_deserialize():
    obj = SalesforceObject()
    response = {"foo": "bar", "baz": "quux"}
    obj.deserialize(response)
    assert obj.foo == "bar"
    assert obj.baz == "quux"


def test_deserialize_group():
    response1 = {"foo": "bar"}
    response2 = {"foo": "bar"}
    objects = SalesforceObject.deserialize_group([response1, response2])
    assert objects[0].foo == "bar"
    assert objects[1].foo == "bar"


def test_getattr():
    obj = SalesforceObject()
    SalesforceObject.attr_to_field_map, SalesforceObject.field_to_attr_map = obj.make_maps(
        ["foo", "bar", "baz"]
    )
    with pytest.raises(AttributeError):
        obj.quux
    with pytest.raises(AttributeError):
        obj.foo  # fails because there's no 'id' attribune
    obj2 = SalesforceObject()
    response = {"id": "a0wS0000002hugV", "baz": "quux"}
    obj2.deserialize(response)
    assert obj2.baz == "quux"
    with pytest.raises(AttributeError):
        obj2.fizzle  # fails because field doesn't exist


def test_check_response():
    response = Response()
    response.status_code = 204
    with pytest.raises(Exception):
        sf.check_response(response)

    assert sf.check_response(response, expected_status=204)

    response.status_code = 500
    with pytest.raises(Exception):
        sf.check_response(response)

    response.status_code = 404
    with pytest.raises(Exception):
        sf.check_response(response)

    response.status_code = 200
    response = sf.check_response(response)
    assert response is True


zone = timezone("US/Central")

today = datetime.now(tz=zone).strftime("%Y-%m-%d")


def test__format_slack():

    opportunity = Opportunity(sf_connection=sf)
    opportunity.account_id = "0011700000BpR8PAAV"
    opportunity.amount = 9
    opportunity.encouraged_by = "Because I love the Trib!"
    opportunity.name = "D C (dcraigmile+test6@texastribune.org)"
    opportunity.stripe_id = "cus_78MqJSBejMN9gn"
    opportunity.agreed_to_pay_fees = True
    opportunity.referral_id = "1234"
    opportunity.lead_source = "Stripe"
    opportunity.description = "The Texas Tribune Membership"
    opportunity.stripe_customer = "cus_78MqJSBejMN9gn"

    rdo = RDO(sf_connection=sf)
    rdo.referral_id = "1234"
    rdo.encouraged_by = "Because I love the Trib!"
    rdo.lead_source = "Stripe"
    rdo.contact_id = "0031700000BHQzBAAX"
    rdo.installment_period = "yearly"
    rdo.stripe_customer = "cus_78MqJSBejMN9gn"
    rdo.amount = 100
    rdo.name = "foo"
    rdo.installments = 3
    rdo.open_ended_status = None
    rdo.description = "Texas Tribune Circle Membership"
    rdo.agreed_to_pay_fees = True
    rdo.type = "Giving Circle"

    contact = Contact(sf_connection=sf)
    contact.email = "dcraigmile+test6@texastribune.org"
    contact.first_name = "D"
    contact.last_name = "C"
    contact.lead_source = "Stripe"
    contact.work_email = "dcraigmile+test6@texastribune.org"

    account = Account(sf_connection=sf)
    account.name = "Acme Inc."
    account.website = "http://acme.com"
    account.shipping_street = "Street"
    account.shipping_city = "Austin"
    account.shipping_postalcode = "78701"
    account.shipping_state = "TX"
    account.record_type_name = "Household"

    actual = construct_slack_message(
        account=account, rdo=rdo, opportunity=None, contact=None
    )
    expected = "Acme Inc. pledged $100 [yearly] (Because I love the Trib!)"

    assert actual == expected
    actual = construct_slack_message(
        account=None, rdo=rdo, opportunity=None, contact=contact
    )
    expected = "D C pledged $100 [yearly] (Because I love the Trib!)"

    assert actual == expected

    actual = construct_slack_message(
        account=None, rdo=None, opportunity=opportunity, contact=contact
    )
    expected = "D C pledged $9 [one-time] (Because I love the Trib!)"

    assert actual == expected


# @patch("npsp.SalesforceObject.get_schema")
# def test__format_opportunity(get_schema):
#     get_schema.return_value = None
#     Opportunity.field_to_attr_map = {
#         "Id": "id",
#         "Amount": "amount",
#         "Name": "name",
#         "Stripe_Customer_ID__c": "stripe_customer_id",
#         "Description": "description",
#         "Stripe_Agreed_to_pay_fees__c": "stripe_agreed_to_pay_fees",
#         "AccountId": "account_id",
#         "CloseDate": "close_date",
#         "Encouraged_to_contribute_by__c": "encouraged_to_contribute_by",
#         "LeadSource": "lead_source",
#         "Referral_ID__c": "referral_id",
#         "StageName": "stage_name",
#         "Type": "type",
#     }

#     opportunity = Opportunity(sf_connection=sf)
#     opportunity.account_id = "0011700000BpR8PAAV"
#     opportunity.amount = 9
#     opportunity.encouraged_to_contribute_by = "Because I love the Trib!"
#     opportunity.name = "D C (dcraigmile+test6@texastribune.org)"
#     opportunity.stripe_customer_id = "cus_78MqJSBejMN9gn"
#     opportunity.stripe_agreed_to_pay_fees = True
#     opportunity.referral_id = "1234"
#     opportunity.lead_source = "Stripe"
#     opportunity.description = "The Texas Tribune Membership"
#     opportunity.stripe_customer_id = "cus_78MqJSBejMN9gn"

#     response = opportunity.serialize()
#     expected = {
#         "AccountId": "0011700000BpR8PAAV",
#         "Amount": 9,
#         "CloseDate": today,
#         "Encouraged_to_contribute_by__c": "Because I love the Trib!",
#         "LeadSource": "Stripe",
#         "Name": "D C (dcraigmile+test6@texastribune.org)",
#         "RecordType": {"Name": "Membership"},
#         "StageName": "Pledged",
#         "Stripe_Customer_ID__c": "cus_78MqJSBejMN9gn",
#         "Referral_ID__c": "1234",
#         "Description": "The Texas Tribune Membership",
#         "Stripe_Agreed_to_pay_fees__c": True,
#         "Type": "Single",
#         "Stripe_Card__c": None,
#         "Stripe_Transaction_ID__c": None,
#         "npsp__Closed_Lost_Reason__c": None,
#         "Stripe_Card_Brand__c": None,
#         "Stripe_Card_Expiration__c": None,
#         "Stripe_Card_Last_4__c": None,
#         "Amazon_Order_Id__c": None,
#     }
#     assert response == expected


# @patch("npsp.SalesforceObject.get_schema")
# def test__format_circle_donation(get_schema):
#     get_schema.return_value = None

#     RDO.field_to_attr_map = {
#         "Id": "id",
#         "Name": "name",
#         "npe03__Amount__c": "amount",
#         "npe03__Contact__c": "contact",
#         "npe03__Installment_Amount__c": "installment_amount",
#         "npe03__Installment_Period__c": "installment_period",
#         "npe03__Installments__c": "installments",
#         "npe03__Open_Ended_Status__c": "open_ended_status",
#         "npe03__Organization__c": "organization",
#         "npe03__Recurring_Donation_Campaign__c": "recurring_donation_campaign",
#         "Type__c": "type",
#         "Lead_Source__c": "lead_source",
#         "Encouraged_to_contribute_by__c": "encouraged_to_contribute_by",
#         "Stripe_Agreed_to_pay_fees__c": "stripe_agreed_to_pay_fees",
#         "Stripe_Card__c": "stripe_card",
#         "Stripe_Customer_Id__c": "stripe_customer_id",
#         "Stripe_Description__c": "stripe_description",
#         "Stripe_Transaction_Id__c": "stripe_transaction_id",
#         "Billing_Email__c": "billing_email",
#         "Blast_Subscription_Email__c": "blast_subscription_email",
#         "Referral_ID__c": "referral_id",
#     }

#     rdo = RDO(sf_connection=sf)
#     rdo.referral_id = "1234"
#     rdo.encouraged_to_contribute_by = "Because I love the Trib!"
#     rdo.lead_source = "Stripe"
#     rdo.contact = "0031700000BHQzBAAX"
#     rdo.installment_period = "yearly"
#     rdo.stripe_customer_id = "cus_78MqJSBejMN9gn"
#     rdo.amount = 100
#     rdo.name = "foo"
#     rdo.installments = 3
#     rdo.open_ended_status = None
#     rdo.stripe_description = "Texas Tribune Circle Membership"
#     rdo.stripe_agreed_to_pay_fees = True
#     rdo.type = "Giving Circle"

#     response = rdo.serialize()
#     expected_response = {
#         "Referral_ID__c": "1234",
#         "Encouraged_to_contribute_by__c": "Because I love the Trib!",
#         "Lead_Source__c": "Stripe",
#         "npe03__Contact__c": "0031700000BHQzBAAX",
#         "npe03__Installment_Period__c": "yearly",
#         "Stripe_Customer_Id__c": "cus_78MqJSBejMN9gn",
#         "npe03__Amount__c": "300.0",  # 3 * 100
#         "Name": "foo",
#         "npe03__Installments__c": 3,
#         "npe03__Open_Ended_Status__c": None,
#         "Stripe_Description__c": "Texas Tribune Circle Membership",
#         "Stripe_Agreed_to_pay_fees__c": True,
#         "Type__c": "Giving Circle",
#         "npe03__Recurring_Donation_Campaign__c": None,
#         "Stripe_Card_Brand__c": None,
#         "Stripe_Card_Expiration__c": None,
#         "Stripe_Card_Last_4__c": None,
#     }
#     assert response == expected_response


# def test__format_cent_circle_donation():

#     rdo = RDO(sf_connection=sf)
#     rdo.referral_id = "1234"
#     rdo.encouraged_to_contribute_by = "Because I love the Trib!"
#     rdo.lead_source = "Stripe"
#     rdo.contact = "0031700000BHQzBAAX"
#     rdo.installment_period = "yearly"
#     rdo.stripe_customer_id = "cus_78MqJSBejMN9gn"
#     rdo.amount = 1501.01
#     rdo.name = "foo"
#     rdo.installments = 3
#     rdo.open_ended_status = None
#     rdo.stripe_description = "Texas Tribune Circle Membership"
#     rdo.stripe_agreed_to_pay_fees = True
#     rdo.type = "Giving Circle"

#     response = rdo.serialize()
#     expected_response = {
#         "Referral_ID__c": "1234",
#         "Encouraged_to_contribute_by__c": "Because I love the Trib!",
#         "Lead_Source__c": "Stripe",
#         "npe03__Contact__c": "0031700000BHQzBAAX",
#         "npe03__Installment_Period__c": "yearly",
#         "Stripe_Customer_Id__c": "cus_78MqJSBejMN9gn",
#         "npe03__Amount__c": "4503.03",  # 3 * 1501.01
#         "Name": "foo",
#         "npe03__Installments__c": 3,
#         "npe03__Open_Ended_Status__c": None,
#         "Stripe_Description__c": "Texas Tribune Circle Membership",
#         "Stripe_Agreed_to_pay_fees__c": True,
#         "Type__c": "Giving Circle",
#         "npe03__Recurring_Donation_Campaign__c": None,
#         "Billing_Email__c": None,
#         "Blast_Subscription_Email__c": None,
#         "Stripe_Card_Brand__c": None,
#         "Stripe_Card_Expiration__c": None,
#         "Stripe_Card_Last_4__c": None,
#     }
#     response["Name"] = "foo"
#     assert response == expected_response


# def test__format_recurring_donation():

#     rdo = RDO(sf_connection=sf)
#     rdo.referral_id = "1234"
#     rdo.encouraged_to_contribute_by = "Because I love the Trib!"
#     rdo.lead_source = "Stripe"
#     rdo.contact = "0031700000BHQzBAAX"
#     rdo.installment_period = "monthly"
#     rdo.stripe_customer_id = "cus_78MqJSBejMN9gn"
#     rdo.amount = 9
#     rdo.name = "foo"
#     rdo.installments = 0
#     rdo.open_ended_status = None
#     rdo.stripe_description = "Texas Tribune Membership"
#     rdo.stripe_agreed_to_pay_fees = True

#     response = rdo.serialize()

#     expected_response = {
#         "Referral_ID__c": "1234",
#         "Encouraged_to_contribute_by__c": "Because I love the Trib!",
#         "Lead_Source__c": "Stripe",
#         "npe03__Contact__c": "0031700000BHQzBAAX",
#         "npe03__Installment_Period__c": "monthly",
#         "Stripe_Customer_Id__c": "cus_78MqJSBejMN9gn",
#         "npe03__Amount__c": 9,
#         "Name": "foo",
#         "npe03__Installments__c": 0,
#         "npe03__Open_Ended_Status__c": None,
#         "Stripe_Description__c": "Texas Tribune Membership",
#         "Stripe_Agreed_to_pay_fees__c": True,
#         "Type__c": "Recurring Donation",
#         "npe03__Recurring_Donation_Campaign__c": None,
#         "Billing_Email__c": None,
#         "Blast_Subscription_Email__c": None,
#         "Stripe_Card_Brand__c": None,
#         "Stripe_Card_Expiration__c": None,
#         "Stripe_Card_Last_4__c": None,
#     }
#     response["Name"] = "foo"
#     assert response == expected_response


# def test__format_recurring_donation_decimal():

#     rdo = RDO(sf_connection=sf)
#     rdo.referral_id = "1234"
#     rdo.encouraged_to_contribute_by = "Because I love the Trib!"
#     rdo.lead_source = "Stripe"
#     rdo.contact = "0031700000BHQzBAAX"
#     rdo.installment_period = "monthly"
#     rdo.stripe_customer_id = "cus_78MqJSBejMN9gn"
#     rdo.amount = 9.15
#     rdo.name = "foo"
#     rdo.installments = 0
#     rdo.open_ended_status = None
#     rdo.stripe_description = "Texas Tribune Membership"
#     rdo.stripe_agreed_to_pay_fees = True

#     response = rdo.serialize()

#     expected_response = {
#         "Referral_ID__c": "1234",
#         "Encouraged_to_contribute_by__c": "Because I love the Trib!",
#         "Lead_Source__c": "Stripe",
#         "npe03__Contact__c": "0031700000BHQzBAAX",
#         "npe03__Installment_Period__c": "monthly",
#         "Stripe_Customer_Id__c": "cus_78MqJSBejMN9gn",
#         "npe03__Amount__c": 9.15,
#         "Name": "foo",
#         "npe03__Installments__c": 0,
#         "npe03__Open_Ended_Status__c": None,
#         "Stripe_Description__c": "Texas Tribune Membership",
#         "Stripe_Agreed_to_pay_fees__c": True,
#         "Type__c": "Recurring Donation",
#         "npe03__Recurring_Donation_Campaign__c": None,
#         "Stripe_Card_Brand__c": None,
#         "Stripe_Card_Expiration__c": None,
#         "Stripe_Card_Last_4__c": None,
#     }
#     response["Name"] = "foo"
#     assert response == expected_response


# def test__format_blast_rdo():

#     rdo = RDO(sf_connection=sf)
#     rdo.referral_id = "1234"
#     rdo.lead_source = "Stripe"
#     rdo.contact = "0031700000BHQzBAAX"
#     rdo.installment_period = "monthly"
#     rdo.stripe_customer_id = "cus_78MqJSBejMN9gn"
#     rdo.amount = 40
#     rdo.name = "foo"
#     rdo.installments = 0
#     rdo.open_ended_status = "Open"
#     rdo.stripe_description = "Monthly Blast Subscription"
#     rdo.stripe_agreed_to_pay_fees = True
#     rdo.type = "The Blast"
#     rdo.billing_email = "dcraigmile+test6@texastribune.org"
#     rdo.blast_subscription_email = "subscriber@foo.bar"

#     response = rdo.serialize()

#     expected_response = {
#         "Referral_ID__c": "1234",
#         "Lead_Source__c": "Stripe",
#         "npe03__Contact__c": "0031700000BHQzBAAX",
#         "npe03__Installment_Period__c": "monthly",
#         "Stripe_Customer_Id__c": "cus_78MqJSBejMN9gn",
#         "npe03__Amount__c": 40,
#         "Name": "foo",
#         "npe03__Installments__c": 0,
#         "npe03__Open_Ended_Status__c": "Open",
#         "Stripe_Description__c": "Monthly Blast Subscription",
#         "Stripe_Agreed_to_pay_fees__c": True,
#         "Type__c": "The Blast",
#         "Billing_Email__c": "dcraigmile+test6@texastribune.org",
#         "Blast_Subscription_Email__c": "subscriber@foo.bar",
#         "npe03__Organization__c": None,
#         "npe03__Recurring_Donation_Campaign__c": None,
#         "Stripe_Card_Brand__c": None,
#         "Stripe_Card_Last_4__c": None,
#         "Stripe_Card_Expiration__c": None,
#     }

#     response["Name"] = "foo"
#     assert response == expected_response


# Contact.field_to_attr_map = {
#     "Id": "id",
#     "AccountId": "account_id",
#     "FirstName": "first_name",
#     "LastName": "last_name",
#     "Email": "email",
#     "LeadSource": "lead_source",
#     "MailingPostalCode": "mailing_postal_code",
# }
# import logging
# import sys

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# with open("Contact.json", "r") as f:
#     contact_schema = json.load(f)


# @patch("npsp.SalesforceConnection.describe")
# def test__format_contact(describe):
#     describe.return_value = contact_schema

#     contact = Contact(sf_connection=sf)
#     contact.email = "dcraigmile+test6@texastribune.org"
#     contact.first_name = "D"
#     contact.last_name = "C"
#     contact.lead_source = "Stripe"
#     contact.work_email = "dcraigmile+test6@texastribune.org"

#     response = contact.serialize()

#     expected_response = {
#         "Email": "dcraigmile+test6@texastribune.org",
#         "FirstName": "D",
#         "LastName": "C",
#         "LeadSource": "Stripe",
#         "npe01__WorkEmail__c": "dcraigmile+test6@texastribune.org",
#     }
#     import pprint

#     pprint.pprint(response)
#     assert response == expected_response


def test_amount_to_charge_cents_just_fees_false():

    opp = Opportunity()
    opp.amount = 10.50
    opp.agreed_to_pay_fees = False

    actual = amount_to_charge(opp)
    expected = Decimal("10.50")
    assert actual == expected


def test_amount_to_charge_just_fees_false():

    opp = Opportunity()
    opp.amount = 10
    opp.agreed_to_pay_fees = False

    actual = amount_to_charge(opp)
    expected = Decimal("10.00")
    assert actual == expected


def test_amount_to_charge_cents_and_fees_true():

    opp = Opportunity()
    opp.amount = 10.50
    opp.agreed_to_pay_fees = True

    actual = amount_to_charge(opp)
    expected = Decimal("11.04")
    assert actual == expected


def test_amount_to_charge_just_fees_true():

    opp = Opportunity()
    opp.amount = 10
    opp.agreed_to_pay_fees = True

    actual = amount_to_charge(opp)
    expected = Decimal("10.53")
    assert actual == expected


def test_make_maps():
    fields = [
        "Id",
        "IsDeleted",
        "AccountId",
        "RecordTypeId",
        "Foo_Bar_Baz__c",
        "Foo_Bar_Baz",
        "Fizzle",
        "swazzle",
        "Jambalaya_c",
    ]
    expected = (
        {
            "id": "Id",
            "is_deleted": "IsDeleted",
            "account_id": "AccountId",
            "record_type_id": "RecordTypeId",
            "Foo_Bar_Baz__c": "Foo_Bar_Baz__c",
            "Foo_Bar_Baz": "Foo_Bar_Baz",
            "fizzle": "Fizzle",
            "swazzle": "swazzle",
            "jambalaya_c": "Jambalaya_c",
        },
        {
            "Id": "id",
            "IsDeleted": "is_deleted",
            "AccountId": "account_id",
            "RecordTypeId": "record_type_id",
            "Foo_Bar_Baz__c": "Foo_Bar_Baz__c",
            "Foo_Bar_Baz": "Foo_Bar_Baz",
            "Fizzle": "fizzle",
            "swazzle": "swazzle",
            "Jambalaya_c": "jambalaya_c",
        },
    )
    actual = Opportunity.make_maps(fields)
    assert actual == expected


def test_deserialize():
    response = {
        "attributes": {
            "type": "Opportunity",
            "url": "/services/data/v43.0/sobjects/Opportunity/0065B00000AeR2yQAF",
        },
        "Id": "0065B00000AeR2yQAF",
        "Amount": 40.0,
        "Name": "Foo Bar Donation (1) 10/15/2018",
        "Stripe_Customer_ID__c": "cus_Dl1EtClmJVKJcp",
        "Description": "Blast Subscription",
        "Stripe_Agreed_to_pay_fees__c": False,
        "AccountId": "0015B00000UiwuKQAR",
    }
    opp = Opportunity()
    opp.deserialize(response)

    assert opp.id == "0065B00000AeR2yQAF"
    assert opp.amount == 40
    assert opp.name == "Foo Bar Donation (1) 10/15/2018"
    assert opp.stripe_customer_id == "cus_Dl1EtClmJVKJcp"
    assert opp.description == "Blast Subscription"
    assert opp.stripe_agreed_to_pay_fees == False
    assert opp.account_id == "0015B00000UiwuKQAR"


def test__getattr():
    # TODO test this better
    opp = Opportunity()
    with pytest.raises(AttributeError):
        opp.foo


def test__setattr():
    # TODO test this more
    opp = Opportunity()
    opp.foo = "bar"
    assert opp.tainted == set()
    opp.foo = "baz"
    assert opp.tainted == set(["foo"])


def test_snake_case():
    assert "account_id" == SalesforceObject.snake_case("AccountId")
    assert "foo_bar" == SalesforceObject.snake_case("abcd__FooBar__c")
    assert "foo_bar" == SalesforceObject.snake_case("abcd__FooBar__c")
    assert "abc_foobar" == SalesforceObject.snake_case("abc_foobar__c")
    assert "abc_foobar" == SalesforceObject.snake_case("abc__foobar__c")
