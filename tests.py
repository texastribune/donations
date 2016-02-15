import json
import re

from unittest.mock import patch
from datetime import datetime
import pytest
from pytz import timezone
import responses
from werkzeug.datastructures import MultiDict

from batch import amount_to_charge
from batch import process_charges
from check_response import check_response
from salesforce import _format_opportunity
from salesforce import _format_recurring_donation
from salesforce import _format_tw_opportunity
from salesforce import SalesforceConnection
from salesforce import upsert_customer


# ("Request: ImmutableMultiDict([('Opportunity.Amount', '100'), ('frequency', "
#  "'until-cancelled'), ('Contact.LastName', 'C'), ('Contact.street', '823 "
#  "Congress Ave Ste 1400'), ('stripeEmail', "
#  "'dcraigmile+test6@texastribune.org'), ('Contact.FirstName', 'D'), "
#  "('Contact.HomePhone', '5551212'), ('stripeToken', "
#  "'tok_16u66IG8bHZDNB6TCq8l3s4p'), ('stripeTokenType', 'card'), "
#  "('Contact.postalCode', '78701')])")


# "Request: ImmutableMultiDict([('frequency', 'one-time'), "
# "('Contact.MailingCity', 'abc'), ('Contact.MailingPostalCode', '78701'), "
# "('Contact.HomePhone', '5551212'), ('Contact.MailingStreet', '123'), "
# "('Opportunity.Amount', '100'), ('stripeToken', "
# "'tok_16vxMhG8bHZDNB6T0QmPd3M4'), ('Reason', 'journalism'), "
# "('Contact.LastName', 'C'), ('stripeEmail', 'dcraigmile@texastribune.org'), "
# "('Description', ''), ('stripeTokenType', 'card'), ('Contact.FirstName', "
# "'D'), ('Contact.MailingState', 'TX')])")


zone = timezone('US/Central')


class CustomerObject(object):
    pass


class RequestObject(object):
    pass


class Customer(object):
    pass

customer = Customer()
customer.id = 'cus_78MqJSBejMN9gn'

# customer = {
#        'account_balance': 0,
#        'created': 1444417221,
#        'currency': None,
#        'default_source': 'card_16u66IG8bHZDNB6T5KL3YJjT',
#        'delinquent': False,
#        'description': None,
#        'discount': None,
#        'email': 'dcraigmile+test6@texastribune.org',
#        'id': 'cus_78MqJSBejMN9gn',
#        'livemode': False,
#        'metadata': {},
#        'object': 'customer',
#        'shipping': None,
#        'sources': {
#            'data': [
#                {
#                    'address_city': None,
#                    'address_country': None,
#                    'address_line1': None,
#                    'address_line1_check': None,
#                    'address_line2': None,
#                    'address_state': None,
#                    'address_zip': None,
#                    'address_zip_check': None,
#                    'brand': 'Visa',
#                    'country': 'US',
#                    'customer': 'cus_78MqJSBejMN9gn',
#                    'cvc_check': 'pass',
#                    'dynamic_last4': None,
#                    'exp_month': 1,
#                    'exp_year': 2016,
#                    'fingerprint': 'emevC9TQ2yGPdnyL',
#                    'funding': 'credit',
#                    'id': 'card_16u66IG8bHZDNB6T5KL3YJjT',
#                    'last4': '4242',
#                    'metadata': {},
#                    'name': 'dcraigmile+test6@texastribune.org',
#                    'object': 'card',
#                    'tokenization_method': None
#                    }
#                ],
#            'has_more': False,
#            'object': 'list',
#            'total_count': 1,
#            'url': '/v1/customers/cus_78MqJSBejMN9gn/sources'
#            },
#        'subscriptions': {
#            'data': [],
#            'has_more': False,
#            'object': 'list',
#            'total_count': 0,
#            'url': '/v1/customers/cus_78MqJSBejMN9gn/subscriptions'
#            }
#        }


# proxy = RequestObject()
# proxy.form = request

contact = {
        'AccountId': '0011700000BpR8PAAV',
        'attributes': {
            'url': '/services/data/v35.0/sobjects/Contact/0031700000BHQzBAAX',
            'type': 'Contact'
            },
        'Stripe_Customer_Id__c': 'cus_78MnnsgVuQb4r6',
        'Id': '0031700000BHQzBAAX'
        }


class Response(object):
    pass


class Request(object):
    pass


request = Request()

form = MultiDict()
form.add('amount', '100')
form.add('frequency', " "'until-cancelled'),
form.add('last_name', 'C'),
form.add('stripeEmail', 'dcraigmile+test6@texastribune.org'),
form.add('first_name', 'D'),
form.add('stripeToken', 'tok_16u66IG8bHZDNB6TCq8l3s4p'),
form.add('stripeTokenType', 'card'),
form.add('reason', 'Because I love the Trib!')
form.add('installment_period', 'yearly')
form.add('installments', '3')
form.add('openended_status', 'None')
form.add('description', 'The Texas Tribune Membership')
form.add('pay_fees_value', 'True')
request.form = form

tw_form = MultiDict()
tw_form.add('amount', '349')
tw_form.add('last_name', 'C'),
tw_form.add('stripeEmail', 'dcraigmile+test6@texastribune.org'),
tw_form.add('first_name', 'D'),
tw_form.add('stripeToken', 'tok_16u66IG8bHZDNB6TCq8l3s4p'),
tw_form.add('stripeTokenType', 'card'),
tw_form.add('description', 'Texas Weekly Subscription')
request.tw_form = tw_form


def test_check_response():
    response = Response()
    response.status_code = 204
    with pytest.raises(Exception):
        check_response(response)

    response.status_code = 500
    with pytest.raises(Exception):
        check_response(response)

    response.status_code = 404
    with pytest.raises(Exception):
        check_response(response)

    response.status_code = 200
    response = check_response(response)
    assert response is True


today = datetime.now(tz=zone).strftime('%Y-%m-%d')


def test__format_opportunity():

    response = _format_opportunity(contact=contact, form=form,
            customer=customer)
    expected_response = {
            'AccountId': '0011700000BpR8PAAV',
            'Amount': '100',
            'CloseDate': today,
            'Encouraged_to_contribute_by__c': 'Because I love the Trib!',
            'LeadSource': 'Stripe',
            'Name': 'D C (dcraigmile+test6@texastribune.org)',
            'RecordTypeId': '01216000001IhI9',
            'StageName': 'Pledged',
            'Stripe_Customer_Id__c': 'cus_78MqJSBejMN9gn',
            'Description': 'The Texas Tribune Membership',
            'Stripe_Agreed_to_pay_fees__c': True,
            'Type': 'Single',
            }

    assert response == expected_response


def test__format_tw_opportunity():

    response = _format_tw_opportunity(contact=contact, form=tw_form,
            customer=customer)
    expected_response = {
            'AccountId': '0011700000BpR8PAAV',
            'Amount': '349',
            'CloseDate': today,
            'LeadSource': 'Stripe',
            'Name': 'DC (dcraigmile+test6@texastribune.org)',
            'RecordTypeId': '01216000001IhQNAA0',
            'Type': 'Single',
            'StageName': 'Pledged',
            'Stripe_Customer_Id__c': 'cus_78MqJSBejMN9gn',
            'Description': 'Texas Weekly Subscription',
            }

    assert response == expected_response


def test__format_recurring_donation():

    response = _format_recurring_donation(contact=contact, form=form,
            customer=customer)
    expected_response = {
            'Encouraged_to_contribute_by__c': 'Because I love the Trib!',
            'npe03__Date_Established__c': today,
            'Lead_Source__c': 'Stripe',
            'npe03__Contact__c': '0031700000BHQzBAAX',
            'npe03__Installment_Period__c': 'yearly',
            'npe03__Open_Ended_Status__c': 'Open',
            'Stripe_Customer_Id__c': 'cus_78MqJSBejMN9gn',
            'npe03__Amount__c': '300',   # 3 * 100
            'Name': 'foo',
            'npe03__Installments__c': '3',
            'npe03__Open_Ended_Status__c': 'None',
            'Stripe_Description__c': 'The Texas Tribune Membership',
            'Stripe_Agreed_to_pay_fees__c': True,
            'Type__c': 'Giving Circle'
            }
    response['Name'] = 'foo'
    assert response == expected_response


def test__format_contact():
    sf = SalesforceConnection()

    response = sf._format_contact(form=form)

    expected_response = {'Description': 'The Texas Tribune Membership',
            'Email': 'dcraigmile+test6@texastribune.org',
            'FirstName': 'D',
            'LastName': 'C',
            'LeadSource': 'Stripe',
            'Stripe_Customer_Id__c': None}

    assert response == expected_response


def test_upsert_empty_customer():
    with pytest.raises(Exception):
        upsert_customer(customer=None, request=None)


def test_upsert_empty_request():
    with pytest.raises(Exception):
        upsert_customer(customer=customer, request=None)


def request_callback(request):
    if 'All_In_One_EMail__c' in request.path_url:
        resp_body = '{"done": true, "records": []}'
    else:
        resp_body = '{"done": true, "records": ["foo"]}'

    return (200, {}, resp_body)


@responses.activate
def test__get_contact():
    url_re = re.compile(r'http://foo/services/data/v35.0/query.*')
    url_re2 = re.compile(r'https://.*salesforce.com/services/oauth2/token')

    responses.add(responses.GET, url_re,
            body='{"done": true, "records": ["foo"]}')
    responses.add(responses.POST, url_re2,
            body='{"instance_url": "http://foo", "errors": [], "id":'
            '"a0917000002rZngAAE", "access_token": "bar", "success": true}',
            status=200)

    sf = SalesforceConnection()
    response = sf._get_contact('schnitzel')
    expected_response = 'foo'
    assert response == expected_response


@responses.activate
def test_create_contact():
    url_re = re.compile(r'http://foo/services/data/v35.0/query.*')
    url_re2 = re.compile(r'https://.*salesforce.com/services/oauth2/token')
    responses.add(responses.GET, url_re,
            body='{"done": true, "records": ["foo"]}')
    responses.add(responses.POST, url_re2,
            body='{"instance_url": "http://foo", "errors": [], "id":'
            '"a0917000002rZngAAE", "access_token": "bar", "success": true}',
            status=200)
    responses.add(responses.POST,
            'http://foo/services/data/v35.0/sobjects/Contact',
            body='{"errors": [], "id": "0031700000F3kcwAAB", "success": true}',
            status=201,)

    sf = SalesforceConnection()
    response = sf.create_contact(form=form)
    expected_response = 'foo'
    assert response == expected_response


@responses.activate
def test_find_contact():
    url_re = re.compile(r'http://foo/services/data/v35.0/query.*')
    url_re2 = re.compile(r'https://.*salesforce.com/services/oauth2/token')
    responses.add(responses.GET, url_re,
            body='{"done": true, "records": ["foo"]}')
    responses.add(responses.POST, url_re2,
            body='{"instance_url": "http://foo", "errors": [], "id":'
            '"a0917000002rZngAAE", "access_token": "bar", "success": true}',
            status=200)

    sf = SalesforceConnection()
    response = sf.find_contact(email='bogus')
    expected_response = ['foo']
    assert response == expected_response


@responses.activate
def test_get_or_create_contact_non_extant():

    # first testing for the case where the user doesn't exist and needs to be
    # created

    url_re2 = re.compile(r'https://.*salesforce.com/services/oauth2/token')
    responses.add(responses.POST, url_re2,
            body='{"instance_url": "http://foo", "errors": [], "id":'
            '"a0917000002rZngAAE", "access_token": "bar", "success": true}',
            status=200)
    responses.add(responses.POST,
            'http://foo/services/data/v35.0/sobjects/Contact',
            body='{"errors": [], "id": "0031700000F3kcwAAB", "success": true}',
            status=201,)
    url_re = re.compile(r'http://foo/services/data/v35.0/query.*')
    responses.add_callback(
            responses.GET, url_re,
            callback=request_callback,
            )

    sf = SalesforceConnection()
    response = sf.get_or_create_contact(form=form)
    # they were created:
    expected_response = (True, 'foo')
    assert response == expected_response


@responses.activate
def test_get_or_create_contact_extant():

    # next we test with the user already extant:
    url_re = re.compile(r'http://foo/services/data/v35.0/query.*')
    url_re2 = re.compile(r'https://.*salesforce.com/services/oauth2/token')
    responses.add(responses.GET, url_re,
            body='{"done": true, "records": ["foo"]}')
    responses.add(responses.POST, url_re2,
            body='{"instance_url": "http://foo", "errors": [], "id":'
            '"a0917000002rZngAAE", "access_token": "bar", "success": true}',
            status=200)

    sf = SalesforceConnection()
    response = sf.get_or_create_contact(form=form)
    # no need to create:
    expected_response = (False, 'foo')
    assert response == expected_response


@responses.activate
def test_get_or_create_contact_multiple():
    # TODO: check that we send an alert

    # next we test with the user already extant:
    url_re = re.compile(r'http://foo/services/data/v35.0/query.*')
    url_re2 = re.compile(r'https://.*salesforce.com/services/oauth2/token')
    responses.add(responses.GET, url_re,
            body='{"done": true, "records": ["foo", "bar"]}')
    responses.add(responses.POST, url_re2,
            body='{"instance_url": "http://foo", "errors": [], "id":'
            '"a0917000002rZngAAE", "access_token": "bar", "success": true}',
            status=200)

    sf = SalesforceConnection()
    response = sf.get_or_create_contact(form=form)
    # no need to create:
    expected_response = (False, 'foo')
    assert response == expected_response


@responses.activate
def test_upsert_non_extant():

    url_re2 = re.compile(r'https://.*salesforce.com/services/oauth2/token')
    responses.add(
            responses.POST, url_re2,
            body='{"instance_url": "http://foo", "errors": [], "id": "a0917000002rZngAAE", "access_token": "bar", "success": true}',
            status=200,
            )
    responses.add(
            responses.POST,
            'http://foo/services/data/v35.0/sobjects/Contact',
            body='{"errors": [], "id": "0031700000F3kcwAAB", "success": true}',
            status=201,
            )
    responses.add_callback(
            responses.GET,
            'http://foo/services/data/v35.0/query',
            callback=request_callback,
            )

    actual = upsert_customer(customer=customer, form=form)
    assert actual is True
    assert len(responses.calls) == 4


list_resp_body = {
        'done': True,
        'records': [
            {'AccountId': '0011700000BpR8PAAV',
                'Id': '0031700000BHQzBAAX',
                'Stripe_Customer_Id__c': 'cus_7GHFg5Dk07Loox',
                'attributes': {'type': 'Contact',
                    'url': '/services/data/v35.0/sobjects/Contact/0031700000BHQzBAAX'}},
            {'AccountId': '0011700000BqjZSAAZ',
                'Id': '0031700000BM3J4AAL',
                'Stripe_Customer_Id__c': None,
                'attributes': {'type': 'Contact',
                    'url': '/services/data/v35.0/sobjects/Contact/0031700000BM3J4AAL'}}
                ],
        'totalSize': 9
        }


def request_upsert_extant_callback(request):
    if 'All_In_One_EMail__c' in request.path_url:
        resp_body = json.dumps(list_resp_body)
    else:
        resp_body = '{"done": true, "records": ["foo"]}'

    return (200, {}, resp_body)


@responses.activate
def test_upsert_extant():

    url_re2 = re.compile(r'https://.*salesforce.com/services/oauth2/token')
    responses.add(
            responses.PATCH,
            'http://foo/services/data/v35.0/sobjects/Contact/0031700000BHQzBAAX',
            body='{"errors": [], "id": "a0917000002rZngAAE", "success": true}',
            status=204,
            )
    responses.add(
            responses.POST, url_re2,
            body='{"instance_url": "http://foo", "errors": [], "id": "a0917000002rZngAAE", "access_token": "bar", "success": true}',
            status=200,
            )
    responses.add(
            responses.POST,
            'http://foo/services/data/v35.0/sobjects/Contact',
            body='{"errors": [], "id": "0031700000F3kcwAAB", "success": true}',
            status=200,
            )
    responses.add_callback(
            responses.GET,
            'http://foo/services/data/v35.0/query',
            callback=request_upsert_extant_callback,
            )

    actual = upsert_customer(customer=customer, form=form)
    assert actual is True
    assert len(responses.calls) == 3


def test_amount_to_charge_just_fees_false():
    foo = {}
    foo['Amount'] = 10
    foo['Stripe_Agreed_to_pay_fees__c'] = False

    actual = amount_to_charge(foo)
    expected = 1000
    assert actual == expected


def test_amount_to_charge_just_fees_true():
    foo = {}
    foo['Amount'] = 10
    foo['Stripe_Agreed_to_pay_fees__c'] = True

    # 10 * 2.9% + $0.30 = $0.59

    actual = amount_to_charge(foo)
    expected = 1059
    assert actual == expected


class RequestsResponse(object):
    status_code = 204


class SourceObject(object):
    id = "bar"


class ChargeReturnValue(object):
    status = "failed"
    id = "foo"
    source = SourceObject()

sf_response = [{'Amount': 84.0,
    'Name': 'D C Donation (1 of 36) 2/11/2016',
    'Stripe_Customer_ID__c': 'cus_7tGeFILs2fuOOd',
    'Stripe_Agreed_to_pay_fees__c': False,
    'Description': 'The Texas Tribune Circle Membership',
    'attributes': {
        'type': 'Opportunity',
        'url': '/services/data/v35.0/sobjects/Opportunity/'
        '006q0000005r5cOAAQ'
        }}]


@patch('batch.requests')
@patch('batch.Log')
@patch('batch.stripe.Charge.create')
@patch('batch.SalesforceConnection.query')
def test_process_failed_charges(sf_connection_query, stripe_charge, log,
        requests_lib):
    """
    It looks like a Stripe charge can fail without raising an
    exception. This tests that we'll log the error and not proceed.

    """
    stripe_charge.return_value = ChargeReturnValue()
    sf_connection_query.return_value = sf_response
    requests_lib.patch.return_value = RequestsResponse()
    process_charges('whatever', log)
    log.it.assert_called_with("Charge failed. Check Stripe logs.")


@patch('batch.requests')
@patch('batch.Log')
@patch('batch.stripe.Charge.create')
@patch('batch.SalesforceConnection.query')
def test_process_success(sf_connection_query, stripe_charge, log,
        requests_lib):
    """
    This tests the normal case where everything succeeds.
    """

    charge_return_value = ChargeReturnValue()
    charge_return_value.status = "succeeded"
    stripe_charge.return_value = charge_return_value
    sf_connection_query.return_value = sf_response
    requests_lib.patch.return_value = RequestsResponse()
    process_charges('whatever', log)
    log.it.assert_called_with("ok")
