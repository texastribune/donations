import json
import requests
import locale
from datetime import datetime
import os

SALESFORCE = {
    "HOST": os.environ['SALESFORCE_HOST'],
    "CLIENT_ID": os.environ['SALESFORCE_CLIENT_ID'],
    "CLIENT_SECRET": os.environ['SALESFORCE_CLIENT_SECRET'],
    "USERNAME": os.environ['SALESFORCE_USERNAME'],
    "PASSWORD": os.environ['SALESFORCE_PASSWORD'],
}

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

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

    def get_account(self, email):
        query = """SELECT AccountId
                    FROM Contact
                    WHERE All_In_One_EMail__c
                    LIKE '%{}%'
                """.format(email)
        response = self.query(query)
        account_id = response[0]['AccountId']
        return account_id

    def add_opp(self, account_id, amount, charge_id, customer_id, card, last_four):
        now = datetime.now().strftime('%Y-%m-%d')
        opportunity = {
                'AccountId': '{}'.format(account_id),
                'StageName': 'Closed Won',
                'Amount': '{}'.format(amount),
                'CloseDate': now,
                'RecordTypeId': '01216000001IhHpAAK',
                'Name': 'test2',
                'last4__c': last_four,
                'Stripe_Customer_ID__c': customer_id,
                'Stripe_Transaction_ID__c': charge_id,
                'Stripe_Card__c': card,
                'LeadSource': 'Stripe',
                # Lead Source
                # the stripe IDs
                # Description
                # Encouraged to Contribute by
                # Co Member First name, last name, and email

                }
        path = '/services/data/v33.0/sobjects/Opportunity'
        url = '{}{}'.format(self.instance_url, path)
        resp = requests.post(url, headers=self.headers, data=json.dumps(opportunity))
        response = json.loads(resp.text)
        print (response)


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
