from datetime import datetime
import json
import locale

import requests
from pytz import timezone

from config import SALESFORCE
from config import DONATION_RECORDTYPEID
#from pprint import pprint  # TODO: remove

# TODO: read environment for the timezone?
zone = timezone('US/Central')

# TODO: insert URLs like this?
# https://dashboard.stripe.com/test/customers/cus_77dLtLXIezcSHe?

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


class SalesforceConnection(object):

    def __init__(self):

        self.payload = {
                'grant_type': 'password',
                'client_id': SALESFORCE['CLIENT_ID'],
                'client_secret': SALESFORCE['CLIENT_SECRET'],
                'username': SALESFORCE['USERNAME'],
                'password': SALESFORCE['PASSWORD'],
                }
        token_path = '/services/oauth2/token'
        self.url = '{}://{}{}'.format('https', SALESFORCE['HOST'],
                token_path)

        # TODO: some error handling here:
        r = requests.post(self.url, data=self.payload)
        print (r)
        print (r.text)
        response = json.loads(r.text)
        print(response)
        self.instance_url = response['instance_url']
        access_token = response['access_token']

        self.headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'X-PrettyPrint': '1',
                'Content-Type': 'application/json'
                }

        return None


    def query(self, query, path='/services/data/v34.0/query'):
        url = '{}{}'.format(self.instance_url, path)
        if query is None:
            payload = {}
        else:
            payload = {'q': query}
        # TODO: error handling:
        r = requests.get(url, headers=self.headers, params=payload)
        response = json.loads(r.text)
        # recursively get the rest of the records:
        if response['done'] is False:
            return response['records'] + self.query(query=None,
                    path=response['nextRecordsUrl'])
        return response['records']

    def post(self, path=None, data=None):
        url = '{}{}'.format(self.instance_url, path)
        resp = requests.post(url, headers=self.headers, data=json.dumps(data))
        response = json.loads(resp.text)
        # pprint(response)
        # pprint(resp)
        print (resp.status_code)
        check_response(response=resp, expected_status=201)
        return response


    def _format_contact(self, request_form=None):

        try:
            stripe_id = request_form['Stripe_Customer_Id__c']
        except KeyError:
            stripe_id = None

        contact = {
            'Email': request_form['stripeEmail'],
            'FirstName': request_form['first_name'],
            'LastName': request_form['last_name'],
            'Description': 'added by Stripe/Checkout app',
            'LeadSource': 'Stripe',
            'Stripe_Customer_Id__c': stripe_id,
            }

        return contact

    def _get_contact(self, contact_id=None):
        """
        We get the contact (after creating it) so that we can find out the ID
        of the account that also created. We need the account so we can tie
        an opportunity to it.
        """

        query = """
                SELECT AccountId
                FROM Contact
                WHERE id = '{}'
                """.format(contact_id)
        # pprint (query)
        response = self.query(query)
        # unlike elsewhere there should only be one result here because we're
        # querying on a 1:1 relationship:
        contact = response[0]
        return contact

    def create_contact(self, request_form):
        """
        Create and return a contact. Then fetch that created contact to get
        the associated account ID.
        """

        print ("----Creating contact...")
        contact = self._format_contact(request_form=request_form)
        path = '/services/data/v34.0/sobjects/Contact'
        response = self.post(path=path, data=contact)
        print(response)
        contact_id = response['id']
        contact = self._get_contact(contact_id)
        return contact

    def find_contact(self, email=None):
        """
        Given an email address return all contacts matching
        it. Returns a list with Account and Stripe IDs.
        """

        query = """
                SELECT AccountId, Id, Stripe_Customer_Id__c
                FROM Contact
                WHERE All_In_One_EMail__c
                LIKE '%{}%'
                """.format(email)
        # pprint (query)
        response = self.query(query)
        return response

    def get_or_create_contact(self, request_form):
        """
        Return a contact. If one already exists it's returned. Otherwise
        a new contact is created and returned.
        """

        created = False

        response = self.find_contact(email=request_form['stripeEmail'])

        # if the response is empty then nothing matched and we
        # have to create a contact:
        if len(response) < 1:
            contact = self.create_contact(request_form)
            created = True
            return created, contact

        elif len(response) > 1:
            print ("more than one result")
            # TODO: send alert because more than one account matched

        return created, response[0]


def check_response(response=None, expected_status=200):
    if response.status_code != expected_status:
        raise Exception("bad")
    return True


def upsert(customer=None, request=None):
    """
    Creates the user if it doesn't exist in Salesforce. If it does exist
    the Stripe Customer ID is added to the Salesforce record.
    """

    if customer is None:
        raise Exception("Value for 'customer' must be specified.")
    if request is None:
        raise Exception("Value for 'request' must be specified.")

    update = {'Stripe_Customer_Id__c': customer.id}
    updated_request = update.copy()
    updated_request.update(request.form.to_dict())

    sf = SalesforceConnection()
    created, contact = sf.get_or_create_contact(updated_request)

    if not created:
        print ("----Exists, updating")
        # pprint (contact)

        path = '/services/data/v34.0/sobjects/Contact/{}'.format(contact['Id'])
        url = '{}{}'.format(sf.instance_url, path)
        print (url)
        resp = requests.patch(url, headers=sf.headers, data=json.dumps(update))
        # TODO: check 'errors' and 'success' too
        print (resp)
        check_response(response=resp, expected_status=204)

    return True


def _format_opportunity(contact=None, request=None, customer=None):
    """
    Format an opportunity for insertion.
    """

    today = datetime.now(tz=zone).strftime('%Y-%m-%d')

    opportunity = {
            'AccountId': '{}'.format(contact['AccountId']),
            'Amount': '{}'.format(request.form['Opportunity.Amount']),
            'CloseDate': today,
            'RecordTypeId': DONATION_RECORDTYPEID,
            'Name': '{}{} ({})'.format(
                request.form['first_name'],
                request.form['last_name'],
                request.form['stripeEmail'],
                ),
            'StageName': 'Pledged',
            'Stripe_Customer_Id__c': customer.id,
#            'Stripe_Transaction_Id__c': charge.id,
#            'Stripe_Card__c': charge.source.id,
            'LeadSource': 'Stripe',
#            'Description': charge.description,
            'Encouraged_to_contribute_by__c': '{}'.format(request.form['Reason']),
            # Co Member First name, last name, and email
            }
    # pprint (opportunity)
    return opportunity


def add_opportunity(request=None, customer=None, charge=None):

    print ("----Adding opportunity...")
    sf = SalesforceConnection()
    _, contact = sf.get_or_create_contact(request.form)
    opportunity = _format_opportunity(contact=contact, request=request,
            customer=customer)
    path = '/services/data/v34.0/sobjects/Opportunity'
    response = sf.post(path=path, data=opportunity)
    # pprint(response)

    return response


def _format_recurring_donation(contact=None, request=None, customer=None):

    today = datetime.now(tz=zone).strftime('%Y-%m-%d')
    now = datetime.now(tz=zone).strftime('%Y-%m-%d %I:%M:%S %p %Z')
    amount = request.form['Opportunity.Amount']

    # TODO: test this
    if request.form['OpenEndedStatus'] == 'None' and (
            request.form['Installments'] == '3' or
            request.form['Installments'] == '36') and (
                    request.form['InstallmentPeriod'] == 'yearly' or
            request.form['InstallmentPeriod'] == 'monthly'):
        type = 'Giving Circle'

    # TODO: test this:
    if request.form['Installments'] is not None:
        amount = int(amount) * int(request.form['Installments'])

    recurring_donation = {
            'npe03__Contact__c': '{}'.format(contact['Id']),
            'npe03__Amount__c': '{}'.format(amount),
            'npe03__Date_Established__c': today,
            'npe03__Open_Ended_Status__c': '',
            'Name': '{} for {} {}'.format(
                now,
                request.form['first_name'],
                request.form['last_name'],
                ),
            'Stripe_Customer_Id__c': customer.id,
            'Lead_Source__c': 'Stripe',
            'Encouraged_to_contribute_by__c': '{}'.format(
                request.form['Reason']),
            'npe03__Open_Ended_Status__c': request.form['OpenEndedStatus'],
            'npe03__Installments__c': request.form['Installments'],
            'npe03__Installment_Period__c': request.form['InstallmentPeriod'],
            'Type__c': type,

            # Co Member First name, last name, and email  TODO
            # Type (Giving Circle, etc) TODO
            }
    return recurring_donation


def add_recurring_donation(request=None, customer=None):

    print ("----Adding recurring donation...")
    sf = SalesforceConnection()
    _, contact = sf.get_or_create_contact(request.form)
    recurring_donation = _format_recurring_donation(contact=contact,
            request=request, customer=customer)
    # pprint (recurring_donation)
    path = '/services/data/v34.0/sobjects/npe03__Recurring_Donation__c'
    response = sf.post(path=path, data=recurring_donation)
    # TODO: error handling
    # pprint(response)

    return True
