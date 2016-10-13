import json
import re

from unittest.mock import patch
from unittest.mock import call

from datetime import datetime
import pytest
import stripe
from pytz import timezone
import responses
from werkzeug.datastructures import MultiDict

from batch import amount_to_charge
from batch import process_charges
from check_response import check_response
from salesforce import _format_opportunity
from salesforce import _format_recurring_donation
from salesforce import _format_blast_rdo
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

circle_form = MultiDict()
circle_form.add('amount', '100')
circle_form.add('frequency', 'until-cancelled'),
circle_form.add('last_name', 'C'),
circle_form.add('stripeEmail', 'dcraigmile+test6@texastribune.org'),
circle_form.add('first_name', 'D'),
circle_form.add('stripeToken', 'tok_16u66IG8bHZDNB6TCq8l3s4p'),
circle_form.add('stripeTokenType', 'card'),
circle_form.add('reason', 'Because I love the Trib!')
circle_form.add('installment_period', 'yearly')
circle_form.add('installments', '3')
circle_form.add('openended_status', 'None')
circle_form.add('description', 'The Texas Tribune Membership')
circle_form.add('pay_fees_value', 'True')
request.circle_form = circle_form

rdo_form = MultiDict()
rdo_form.add('amount', '9')
rdo_form.add('frequency', 'until-cancelled'),
rdo_form.add('last_name', 'C'),
rdo_form.add('stripeEmail', 'dcraigmile+test6@texastribune.org'),
rdo_form.add('first_name', 'D'),
rdo_form.add('stripeToken', 'tok_16u66IG8bHZDNB6TCq8l3s4p'),
rdo_form.add('stripeTokenType', 'card'),
rdo_form.add('reason', 'Because I love the Trib!')
rdo_form.add('installment_period', 'monthly')
rdo_form.add('installments', 'None')
rdo_form.add('openended_status', 'None')
rdo_form.add('description', 'The Texas Tribune Membership')
rdo_form.add('pay_fees_value', 'True')
request.rdo_form = rdo_form

blast_rdo_form = MultiDict()
blast_rdo_form.add('amount', '40')
blast_rdo_form.add('frequency', 'until-cancelled'),
blast_rdo_form.add('last_name', 'C'),
blast_rdo_form.add('stripeEmail', 'dcraigmile+test6@texastribune.org'),
blast_rdo_form.add('first_name', 'D'),
blast_rdo_form.add('stripeToken', 'tok_16u66IG8bHZDNB6TCq8l3s4p'),
blast_rdo_form.add('stripeTokenType', 'card'),
blast_rdo_form.add('installment_period', 'monthly')
blast_rdo_form.add('installments', 'None')
blast_rdo_form.add('openended_status', 'None')
blast_rdo_form.add('description', 'Monthly Blast Subscription')
blast_rdo_form.add('subscriber_email', 'subscriber@foo.bar')
blast_rdo_form.add('pay_fees_value', 'True')
request.blast_rdo_form = blast_rdo_form


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

    response = _format_opportunity(contact=contact, form=rdo_form,
            customer=customer)
    expected_response = {
            'AccountId': '0011700000BpR8PAAV',
            'Amount': '9',
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


def test__format_circle_donation():

    response = _format_recurring_donation(contact=contact, form=circle_form,
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


def test__format_recurring_donation():

    response = _format_recurring_donation(contact=contact, form=rdo_form,
            customer=customer)
    expected_response = {
            'Encouraged_to_contribute_by__c': 'Because I love the Trib!',
            'npe03__Date_Established__c': today,
            'Lead_Source__c': 'Stripe',
            'npe03__Contact__c': '0031700000BHQzBAAX',
            'npe03__Installment_Period__c': 'monthly',
            'Stripe_Customer_Id__c': 'cus_78MqJSBejMN9gn',
            'npe03__Amount__c': '9',
            'Name': 'foo',
            'npe03__Installments__c': 0,
            'npe03__Open_Ended_Status__c': 'None',
            'Stripe_Description__c': 'The Texas Tribune Membership',
            'Stripe_Agreed_to_pay_fees__c': True,
            'Type__c': 'Recurring Donation'
            }
    response['Name'] = 'foo'
    assert response == expected_response


def test__format_blast_rdo():

    response = _format_blast_rdo(contact=contact, form=blast_rdo_form,
            customer=customer)
    expected_response = {
            'npe03__Date_Established__c': today,
            'Lead_Source__c': 'Stripe',
            'npe03__Contact__c': '0031700000BHQzBAAX',
            'npe03__Installment_Period__c': 'monthly',
            'Stripe_Customer_Id__c': 'cus_78MqJSBejMN9gn',
            'npe03__Amount__c': '40',
            'Name': 'foo',
            'npe03__Installments__c': 0,
            'npe03__Open_Ended_Status__c': 'Open',
            'Stripe_Description__c': 'Monthly Blast Subscription',
            'Stripe_Agreed_to_pay_fees__c': False,
            'Type__c': 'The Blast',
            'Billing_Email__c': 'dcraigmile+test6@texastribune.org',
            'Blast_Subscription_Email__c': 'subscriber@foo.bar',
            }

    response['Name'] = 'foo'
    assert response == expected_response


def test__format_contact():
    sf = SalesforceConnection()

    response = sf._format_contact(form=rdo_form)

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
    response = sf.create_contact(form=rdo_form)
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
    response = sf.get_or_create_contact(form=rdo_form)
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
    response = sf.get_or_create_contact(form=rdo_form)
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
    response = sf.get_or_create_contact(form=rdo_form)
    # no need to create:
    expected_response = (False, 'foo')
    assert response == expected_response


@responses.activate
def test_upsert_non_extant():

    url_re2 = re.compile(r'https://.*salesforce.com/services/oauth2/token')
    responses.add(
            responses.POST, url_re2,
            body='{"instance_url": "http://foo", "errors": [], "id": "a0917000'
            '002rZngAAE", "access_token": "bar", "success": true}',
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

    actual = upsert_customer(customer=customer, form=rdo_form)
    assert actual is True
    assert len(responses.calls) == 4


list_resp_body = {
        'done': True,
        'records': [
            {'AccountId': '0011700000BpR8PAAV',
                'Id': '0031700000BHQzBAAX',
                'Stripe_Customer_Id__c': 'cus_7GHFg5Dk07Loox',
                'attributes': {'type': 'Contact',
                    'url': '/services/data/v35.0/sobjects/Contact/0031700000BH'
                    'QzBAAX'}},
            {'AccountId': '0011700000BqjZSAAZ',
                'Id': '0031700000BM3J4AAL',
                'Stripe_Customer_Id__c': None,
                'attributes': {'type': 'Contact',
                    'url': '/services/data/v35.0/sobjects/Contact/0031700000BM'
                    '3J4AAL'}}
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
            'http://foo/services/data/v35.0/sobjects/Contact/0031700000BHQzBA'
            'AX',
            body='{"errors": [], "id": "a0917000002rZngAAE", "success": true}',
            status=204,
            )
    responses.add(
            responses.POST, url_re2,
            body='{"instance_url": "http://foo", "errors": [], "id": "a0917000'
            '002rZngAAE", "access_token": "bar", "success": true}',
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

    actual = upsert_customer(customer=customer, form=rdo_form)
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

sf_response_2 = [
        {'Amount': 84.0,
            'Name': 'D C Donation (1 of 36) 2/11/2016',
            'Stripe_Customer_ID__c': 'cus_7tGeFILs2fuOOd',
            'Stripe_Agreed_to_pay_fees__c': False,
            'Description': 'The Texas Tribune Circle Membership',
            'attributes': {
                'type': 'Opportunity',
                'url': '/services/data/v35.0/sobjects/Opportunity/'
                '006q0000005r5cOAAQ'
                }},
        {'Amount': 36.0,
            'Name': 'D C Donation (1 of 36) 2/11/2016',
            'Stripe_Customer_ID__c': 'cus_7tGeFILs2fuOOd',
            'Stripe_Agreed_to_pay_fees__c': False,
            'Description': 'The Texas Tribune Circle Membership',
            'attributes': {
                'type': 'Opportunity',
                'url': '/services/data/v35.0/sobjects/Opportunity/'
                '006q0000005r5cOAAQ'
                }}
            ]


@patch('batch.requests')
@patch('batch.Log')
@patch('batch.stripe.Charge.create')
@patch('batch.SalesforceConnection.query')
def test_fail_continues(sf_connection_query, stripe_charge, log,
        requests_lib):
    """
    This shows that processing will continue even when an error is encountered.
    """
    expected_call_list = [
            call('Found 2 opportunities available to process.'),
            call('---- Charging $84.0 to cus_7tGeFILs2fuOOd (D C Donation (1 o'
            'f 36) 2/11/2016)'),
            call('Problem: '),
            call('---- Charging $36.0 to cus_7tGeFILs2fuOOd (D C Donation (1 o'
            'f 36) 2/11/2016)'),
            call('ok')
            ]

    charge_return_value = ChargeReturnValue()
    charge_return_value.status = "succeeded"
    # stripe_charge.return_value = charge_return_value
    stripe_charge.side_effect = [Exception, charge_return_value]
    sf_connection_query.return_value = sf_response_2
    requests_lib.patch.return_value = RequestsResponse()
    process_charges('whatever', log)
    log.it.assert_called_with("ok")
    print(log.it.call_args_list)
    assert len(log.it.call_args_list) == 5
    assert log.it.call_args_list == expected_call_list


@patch('batch.requests')
@patch('batch.Log')
@patch('batch.stripe.Charge.create')
@patch('batch.SalesforceConnection.query')
def test_card_error(sf_connection_query, stripe_charge, log,
        requests_lib):
    """
    This tests CardErrors from Stripe.
    """
    expected_call_list = [
            call('Found 1 opportunities available to process.'),
            call('---- Charging $84.0 to cus_7tGeFILs2fuOOd (D C Donation (1 o'
            'f 36) 2/11/2016)'),
            call('The card has been declined:'),
            call('\tStatus: 402'),
            call('\tType: card_error'),
            call('\tCode: card_declined'),
            call('\tParam: param'),
            call('\tMessage: message'),
            call('\tDecline code: decline_code')
            ]

    # this is confusing because it's a dict, not JSON
    # but that's what Stripe calls it. See https://stripe.com/docs/api#errors
    json_body = {
            'error': {
                'decline_code': 'decline_code',
                'type': 'card_error',
                'message': 'message',
                'param': 'param',
                'code': 'card_declined',
                }
            }
    stripe_error = stripe.error.CardError(message="message", param="param",
            code="code", json_body=json_body, http_status=402)
    charge_return_value = ChargeReturnValue()
    charge_return_value.status = "succeeded"
    stripe_charge.side_effect = stripe_error
    sf_connection_query.return_value = sf_response
    requests_lib.patch.return_value = RequestsResponse()
    process_charges('whatever', log)
    print (log.it.call_args_list)
    assert len(log.it.call_args_list) == 9
    assert log.it.call_args_list == expected_call_list
