import json
import requests
import locale
from datetime import datetime
import os
import collections

SALESFORCE = {
    "HOST": os.environ['SALESFORCE_HOST'],
    "CLIENT_ID": os.environ['SALESFORCE_CLIENT_ID'],
    "CLIENT_SECRET": os.environ['SALESFORCE_CLIENT_SECRET'],
    "USERNAME": os.environ['SALESFORCE_USERNAME'],
    "PASSWORD": os.environ['SALESFORCE_PASSWORD'],
}

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

ContactAccount = collections.namedtuple('ContactAccount', 'contact account')

class SalesforceConnection(object):


    def __init__(self):

        payload = {
                'grant_type': 'password',
                'client_id': SALESFORCE['CLIENT_ID'],
                'client_secret': SALESFORCE['CLIENT_SECRET'],
                'username': SALESFORCE['USERNAME'],
                'password': SALESFORCE['PASSWORD'],
                }
        token_path = '/services/oauth2/token'
        url = '{}://{}{}'.format('https', SALESFORCE['HOST'],
                token_path)
        # TODO: some error handling here:
        r = requests.post(url, data=payload)
        response = json.loads(r.text)
        self.instance_url = response['instance_url']
        access_token = response['access_token']

        self.headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'X-PrettyPrint': '1',
                'Content-Type': 'application/json'
                }


    def query(self, query, path='/services/data/v33.0/query'):
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


    def create_contact(self, request):

        contact = {
            'Email': request['stripeEmail'],
            'Description': 'added by Stripe/Checkout app',
            'FirstName': request['Contact.FirstName'],
            'LastName': request['Contact.LastName'],
            'HomePhone': request['Contact.HomePhone'],
            'MailingCity': 'Austin',
            'MailingPostalCode': request['Contact.postalCode'],
#            'MailingPostalCode': request['Contact.MailingPostalCode'],
            'MailingState': 'TX',
#            'MailingStreet': request['Contact.MailingStreet'],
            'MailingStreet': request['Contact.street'],
            'LeadSource': 'Stripe',
            }

        path = '/services/data/v33.0/sobjects/Contact'
        url = '{}{}'.format(self.instance_url, path)
        resp = requests.post(url, headers=self.headers, data=json.dumps(contact))
        response = json.loads(resp.text)
        contact_id = response['id']
        query = """SELECT AccountId FROM Contact WHERE id = '{}'""".format(contact_id)
        response = self.query(query)
        # unlike elsewhere there should only be one result here because we're
        # querying on a 1:1 relationship:
        return ContactAccount(contact=contact_id, account=response[0]['AccountId'])

    def get_or_create_account(self, request):

        email = request['stripeEmail']
        query = """SELECT AccountId, Id
                    FROM Contact
                    WHERE All_In_One_EMail__c
                    LIKE '%{}%'
                """.format(email)
        response = self.query(query)

        if len(response) == 1:
            account_id = response[0]['AccountId']
            contact_id = response[0]['Id']
            contact_account = ContactAccount(contact=contact_id, account=account_id)
        elif len(response) > 1:
            # More than one account matches. Let's add it to the first one we found
            # but raise a warning:
            print ("more than one result")
            account_id = response[0]['AccountId']
            contact_id = response[0]['Id']
            contact_account = ContactAccount(contact=contact_id, account=account_id)
            # TODO: send alert
        elif len(response) < 1:
            contact_account = self.create_contact(request)

# [{'AccountId': '0011700000BpR8PAAV', 'attributes': {'type': 'Contact', 'url': '/services/data/v33.0/sobjects/Contact/0031700000BHQzBAAX'}}, {'AccountId': '0011700000BqjZSAAZ', 'attributes': {'type': 'Contact', 'url': '/services/data/v33.0/sobjects/Contact/0031700000BM3J4AAL'}}]

#{'Name': 'test2', 'AccountId': '0011700000BpR8PAAV', 'RecordTypeId': '01216000001IhHpAAK', 'CloseDate': '2015-10-02', 'Stripe_Transaction_ID__c': 'ch_16rIZfG8bHZDNB6TmUE9u7Ej', 'Encouraged_to_contribute_by__c': 'I heart the Trib!', 'Description': 'Change Me', 'Amount': '100.0', 'Stripe_Card__c': 'card_16rIZbG8bHZDNB6TY0auxz2i', 'LeadSource': 'Stripe', 'Stripe_Customer_ID__c': 'cus_75TWyYoU5MKJOX', 'StageName': 'Closed Won'}

        return contact_account

    def get_or_create_contact(self, request):

        email = request['stripeEmail']
        query = """SELECT Id
                    FROM Contact
                    WHERE All_In_One_EMail__c
                    LIKE '%{}%'
                """.format(email)
        response = self.query(query)


        if len(response) == 1:
            contact_id = response[0]['Id']
        elif len(response) > 1:
            # More than one account matches. Let's add it to the first one we found
            # but raise a warning:
            print ("more than one result")
            contact_id = response[0]['Id']
            # TODO: send alert
        elif len(response) < 1:
            contact_id = self.create_contact(request).contact

# [{'AccountId': '0011700000BpR8PAAV', 'attributes': {'type': 'Contact', 'url': '/services/data/v33.0/sobjects/Contact/0031700000BHQzBAAX'}}, {'AccountId': '0011700000BqjZSAAZ', 'attributes': {'type': 'Contact', 'url': '/services/data/v33.0/sobjects/Contact/0031700000BM3J4AAL'}}]

#{'Name': 'test2', 'AccountId': '0011700000BpR8PAAV', 'RecordTypeId': '01216000001IhHpAAK', 'CloseDate': '2015-10-02', 'Stripe_Transaction_ID__c': 'ch_16rIZfG8bHZDNB6TmUE9u7Ej', 'Encouraged_to_contribute_by__c': 'I heart the Trib!', 'Description': 'Change Me', 'Amount': '100.0', 'Stripe_Card__c': 'card_16rIZbG8bHZDNB6TY0auxz2i', 'LeadSource': 'Stripe', 'Stripe_Customer_ID__c': 'cus_75TWyYoU5MKJOX', 'StageName': 'Closed Won'}

        return account_id



def add_opportunity(request=None, customer=None, charge=None, reason=None):

    sf = SalesforceConnection()
    account_id = sf.get_or_create_account(request)
    now = datetime.now().strftime('%Y-%m-%d')

    opportunity = {
            'AccountId': '{}'.format(account_id),
            'StageName': 'Closed Won',
            'Amount': '{}'.format(charge.amount / 100),
            'CloseDate': now,
            'RecordTypeId': '01216000001IhHpAAK',  #TODO: magic number
            'Name': 'TODO',
            'Stripe_Customer_ID__c': customer.id,
            'Stripe_Transaction_ID__c': charge.id,
            'Stripe_Card__c': charge.source.id,
            'LeadSource': 'Stripe',
            'Description': charge.description,
            'Encouraged_to_contribute_by__c': reason,
            # Co Member First name, last name, and email
            }
    print (opportunity)
    path = '/services/data/v33.0/sobjects/Opportunity'
    url = '{}{}'.format(sf.instance_url, path)
    resp = requests.post(url, headers=sf.headers, data=json.dumps(opportunity))
    response = json.loads(resp.text)
#    {'errors': [], 'success': True, 'id': '00617000005g6PBAAY'}


def add_recurring_donation(request=None, customer=None, charge=None, reason=None):

    sf = SalesforceConnection()
    contact_account = sf.get_or_create_account(request)
    now = datetime.now().strftime('%Y-%m-%d')
    recurring_donation = {
            'npe03__Contact__c': '{}'.format(contact_account.contact),
            'npe03__Amount__c': '{}'.format(charge.amount / 100),
            'npe03__Date_Established__c': now,
            'npe03__Open_Ended_Status__c': '',
            'Name': 'TODO',
            'Stripe_Customer_ID__c': customer.id,
            'Stripe_Transaction_ID__c': charge.id,
            'Stripe_Card__c': charge.source.id,
            'Lead_Source__c': 'Stripe', # TODO: this is showing as Givalike in SF; probably a trigger to remove
            'Encouraged_to_contribute_by__c': reason,
            # Co Member First name, last name, and email
            # Type (Giving Circle, etc)
            # TODO: set open-ended status
            }
    print (recurring_donation)
    path = '/services/data/v33.0/sobjects/npe03__Recurring_Donation__c'
    url = '{}{}'.format(sf.instance_url, path)
    resp = requests.post(url, headers=sf.headers, data=json.dumps(recurring_donation))
    response = json.loads(resp.text)
    #TODO: error handling
    print (response)
