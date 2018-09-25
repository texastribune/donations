from datetime import datetime
from decimal import Decimal
from pytz import timezone

import pytest
from batch import amount_to_charge
from npsp import RDO, Contact, Opportunity
import npsp
from util import clean


class SalesforceConnectionSubClass(npsp.SalesforceConnection):
    def __init__(self):
        pass


sf = SalesforceConnectionSubClass()


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


def test__format_amount():
    opp = Opportunity(sf_connection=sf)

    opp.amount = "1500.123"
    actual = opp.amount
    expected = "1500.12"
    assert actual == expected

    opp.amount = "1500"
    actual = opp.amount
    expected = "1500.00"
    assert actual == expected

    opp.amount = "1500.00"
    actual = opp.amount
    expected = "1500.00"
    assert actual == expected

    opp.amount = "1500.126"
    actual = opp.amount
    expected = "1500.13"
    assert actual == expected


class Response(object):
    pass


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


def test__format_opportunity():

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

    response = opportunity._format()
    expected = {
        "AccountId": "0011700000BpR8PAAV",
        "CampaignId": None,
        "Amount": "9.00",
        "CloseDate": today,
        "Encouraged_to_contribute_by__c": "Because I love the Trib!",
        "LeadSource": "Stripe",
        "Name": "D C (dcraigmile+test6@texastribune.org)",
        "RecordTypeId": "01216000001IhI9",
        "StageName": "Pledged",
        "Stripe_Customer_ID__c": "cus_78MqJSBejMN9gn",
        "Referral_ID__c": "1234",
        "Description": "The Texas Tribune Membership",
        "Stripe_Agreed_to_pay_fees__c": True,
        "Type": "Single",
        "Stripe_Card__c": None,
        "Stripe_Transaction_ID__c": None,
        "npsp__Closed_Lost_Reason__c": None,
    }
    assert response == expected


def test__format_circle_donation():

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

    response = rdo._format()
    expected_response = {
        "Referral_ID__c": "1234",
        "Encouraged_to_contribute_by__c": "Because I love the Trib!",
        "npe03__Date_Established__c": today,
        "Lead_Source__c": "Stripe",
        "npe03__Contact__c": "0031700000BHQzBAAX",
        "npe03__Installment_Period__c": "yearly",
        "Stripe_Customer_ID__c": "cus_78MqJSBejMN9gn",
        "Billing_Email__c": None,
        "Blast_Subscription_Email__c": None,
        "npe03__Organization__c": None,
        "npe03__Amount__c": "300.0",  # 3 * 100
        "Name": "foo",
        "npe03__Installments__c": 3,
        "npe03__Open_Ended_Status__c": None,
        "Stripe_Description__c": "Texas Tribune Circle Membership",
        "Stripe_Agreed_to_pay_fees__c": True,
        "Type__c": "Giving Circle",
        "npe03__Recurring_Donation_Campaign__c": None,
    }
    assert response == expected_response


def test__format_cent_circle_donation():

    rdo = RDO(sf_connection=sf)
    rdo.referral_id = "1234"
    rdo.encouraged_by = "Because I love the Trib!"
    rdo.lead_source = "Stripe"
    rdo.contact_id = "0031700000BHQzBAAX"
    rdo.installment_period = "yearly"
    rdo.stripe_customer = "cus_78MqJSBejMN9gn"
    rdo.amount = 1501.01
    rdo.name = "foo"
    rdo.installments = 3
    rdo.open_ended_status = None
    rdo.description = "Texas Tribune Circle Membership"
    rdo.agreed_to_pay_fees = True
    rdo.type = "Giving Circle"

    response = rdo._format()
    expected_response = {
        "Referral_ID__c": "1234",
        "Encouraged_to_contribute_by__c": "Because I love the Trib!",
        "npe03__Date_Established__c": today,
        "Lead_Source__c": "Stripe",
        "npe03__Organization__c": None,
        "npe03__Contact__c": "0031700000BHQzBAAX",
        "npe03__Installment_Period__c": "yearly",
        "Stripe_Customer_ID__c": "cus_78MqJSBejMN9gn",
        "npe03__Amount__c": "4503.03",  # 3 * 1501.01
        "Name": "foo",
        "npe03__Installments__c": 3,
        "npe03__Open_Ended_Status__c": None,
        "Stripe_Description__c": "Texas Tribune Circle Membership",
        "Stripe_Agreed_to_pay_fees__c": True,
        "Type__c": "Giving Circle",
        "npe03__Recurring_Donation_Campaign__c": None,
        "Billing_Email__c": None,
        "Blast_Subscription_Email__c": None,
    }
    response["Name"] = "foo"
    assert response == expected_response


def test__format_recurring_donation():

    rdo = RDO(sf_connection=sf)
    rdo.referral_id = "1234"
    rdo.encouraged_by = "Because I love the Trib!"
    rdo.lead_source = "Stripe"
    rdo.contact_id = "0031700000BHQzBAAX"
    rdo.installment_period = "monthly"
    rdo.stripe_customer = "cus_78MqJSBejMN9gn"
    rdo.amount = 9
    rdo.name = "foo"
    rdo.installments = 0
    rdo.open_ended_status = None
    rdo.description = "Texas Tribune Membership"
    rdo.agreed_to_pay_fees = True

    response = rdo._format()

    expected_response = {
        "Referral_ID__c": "1234",
        "npe03__Organization__c": None,
        "Encouraged_to_contribute_by__c": "Because I love the Trib!",
        "npe03__Date_Established__c": today,
        "Lead_Source__c": "Stripe",
        "npe03__Contact__c": "0031700000BHQzBAAX",
        "npe03__Installment_Period__c": "monthly",
        "Stripe_Customer_ID__c": "cus_78MqJSBejMN9gn",
        "npe03__Amount__c": "9.00",
        "Name": "foo",
        "npe03__Installments__c": 0,
        "npe03__Open_Ended_Status__c": None,
        "Stripe_Description__c": "Texas Tribune Membership",
        "Stripe_Agreed_to_pay_fees__c": True,
        "Type__c": "Recurring Donation",
        "npe03__Recurring_Donation_Campaign__c": None,
        "Billing_Email__c": None,
        "Blast_Subscription_Email__c": None,
    }
    response["Name"] = "foo"
    assert response == expected_response


def test__format_recurring_donation_decimal():

    rdo = RDO(sf_connection=sf)
    rdo.referral_id = "1234"
    rdo.encouraged_by = "Because I love the Trib!"
    rdo.lead_source = "Stripe"
    rdo.contact_id = "0031700000BHQzBAAX"
    rdo.installment_period = "monthly"
    rdo.stripe_customer = "cus_78MqJSBejMN9gn"
    rdo.amount = 9.15
    rdo.name = "foo"
    rdo.installments = 0
    rdo.open_ended_status = None
    rdo.description = "Texas Tribune Membership"
    rdo.agreed_to_pay_fees = True

    response = rdo._format()

    expected_response = {
        "Referral_ID__c": "1234",
        "npe03__Organization__c": None,
        "Billing_Email__c": None,
        "Encouraged_to_contribute_by__c": "Because I love the Trib!",
        "npe03__Date_Established__c": today,
        "Lead_Source__c": "Stripe",
        "Blast_Subscription_Email__c": None,
        "npe03__Contact__c": "0031700000BHQzBAAX",
        "npe03__Installment_Period__c": "monthly",
        "Stripe_Customer_ID__c": "cus_78MqJSBejMN9gn",
        "npe03__Amount__c": "9.15",
        "Name": "foo",
        "npe03__Installments__c": 0,
        "npe03__Open_Ended_Status__c": None,
        "Stripe_Description__c": "Texas Tribune Membership",
        "Stripe_Agreed_to_pay_fees__c": True,
        "Type__c": "Recurring Donation",
        "npe03__Recurring_Donation_Campaign__c": None,
    }
    response["Name"] = "foo"
    assert response == expected_response


def test__format_blast_rdo():

    rdo = RDO(sf_connection=sf)
    rdo.referral_id = "1234"
    rdo.lead_source = "Stripe"
    rdo.contact_id = "0031700000BHQzBAAX"
    rdo.installment_period = "monthly"
    rdo.stripe_customer = "cus_78MqJSBejMN9gn"
    rdo.amount = 40
    rdo.name = "foo"
    rdo.installments = 0
    rdo.open_ended_status = "Open"
    rdo.description = "Monthly Blast Subscription"
    rdo.agreed_to_pay_fees = True
    rdo.type = "The Blast"
    rdo.billing_email = "dcraigmile+test6@texastribune.org"
    rdo.blast_subscription_email = "subscriber@foo.bar"

    response = rdo._format()

    expected_response = {
        "Referral_ID__c": "1234",
        "Encouraged_to_contribute_by__c": None,
        "npe03__Date_Established__c": today,
        "Lead_Source__c": "Stripe",
        "npe03__Contact__c": "0031700000BHQzBAAX",
        "npe03__Installment_Period__c": "monthly",
        "Stripe_Customer_ID__c": "cus_78MqJSBejMN9gn",
        "npe03__Amount__c": "40.00",
        "Name": "foo",
        "npe03__Installments__c": 0,
        "npe03__Open_Ended_Status__c": "Open",
        "Stripe_Description__c": "Monthly Blast Subscription",
        "Stripe_Agreed_to_pay_fees__c": True,
        "Type__c": "The Blast",
        "Billing_Email__c": "dcraigmile+test6@texastribune.org",
        "Blast_Subscription_Email__c": "subscriber@foo.bar",
        "npe03__Organization__c": None,
        "npe03__Recurring_Donation_Campaign__c": None,
    }

    response["Name"] = "foo"
    assert response == expected_response


def test__format_contact():

    contact = Contact(sf_connection=sf)
    contact.email = "dcraigmile+test6@texastribune.org"
    contact.first_name = "D"
    contact.last_name = "C"
    contact.lead_source = "Stripe"

    response = contact._format()

    expected_response = {
        "Email": "dcraigmile+test6@texastribune.org",
        "FirstName": "D",
        "LastName": "C",
        "LeadSource": "Stripe",
        "MailingPostalCode": None,
    }

    assert response == expected_response


def test_amount_to_charge_cents_just_fees_false():

    actual = amount_to_charge(amount=10.50, pay_fees=False)
    expected = Decimal("10.50")
    assert actual == expected


def test_amount_to_charge_just_fees_false():

    actual = amount_to_charge(amount=10, pay_fees=False)
    expected = Decimal("10.00")
    assert actual == expected


def test_amount_to_charge_cents_and_fees_true():

    actual = amount_to_charge(amount=10.50, pay_fees=True)
    expected = Decimal("11.04")
    assert actual == expected


def test_amount_to_charge_just_fees_true():

    actual = amount_to_charge(amount=10, pay_fees=True)
    expected = Decimal("10.53")
    assert actual == expected
