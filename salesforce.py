from datetime import datetime
import json
import locale

import celery
import requests
from pytz import timezone

from config import SALESFORCE
from config import DONATION_RECORDTYPEID
from config import TIMEZONE
from config import ENABLE_SLACK
from config import SLACK_API_KEY
from config import SLACK_CHANNEL

from emails import send_email

zone = timezone(TIMEZONE)

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

WARNINGS = dict()

# TODO: use v35 of Salesforce API
# TODO: use latest version of Stripe API


def notify_slack(message):
    """
    Send a notification about a donation to Slack.
    """
    if ENABLE_SLACK:
        payload = {
                'token': SLACK_API_KEY,
                'channel': SLACK_CHANNEL,
                'text': message,
                }
        url = 'https://slack.com/api/chat.postMessage'
        requests.get(url, params=payload)


def warn_multiple_accounts(email, count):
    """
    Track warnings about multiple accounts (so we don't send
    duplicate warnings about duplicates)
    """
    WARNINGS[email] = count


def send_multiple_account_warning():
    """
    Send the warnings about multiple accounts.
    """

    for email in WARNINGS:
        count = WARNINGS[email]
        body = """
        {} accounts were found matching the email address <{}>
        while inserting a Stripe transaction.

        The transaction was attached to the first match found. You may want to
        move the transaction to the proper account if the one chosen is not
        correct. You may also want to delete or otherwise correct the duplicate
        account(s).
        """.format(count, email)

        send_email(
                recipient='dcraigmile@texastribune.org',
                subject="Multiple accounts found for {}".format(email),
                body=body
                )


class SalesforceConnection(object):
    """
    Represents the Salesforce API.
    """

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

        r = requests.post(self.url, data=self.payload)
        check_response(r)
        response = json.loads(r.text)

        self.instance_url = response['instance_url']
        access_token = response['access_token']

        self.headers = {
                'Authorization': 'Bearer {}'.format(access_token),
                'X-PrettyPrint': '1',
                'Content-Type': 'application/json'
                }

        return None

    def query(self, query, path='/services/data/v34.0/query'):
        """
        Call the Salesforce API to do SOQL queries.
        """
        url = '{}{}'.format(self.instance_url, path)
        if query is None:
            payload = {}
        else:
            payload = {'q': query}
        r = requests.get(url, headers=self.headers, params=payload)
        check_response(r)
        response = json.loads(r.text)
        # recursively get the rest of the records:
        if response['done'] is False:
            return response['records'] + self.query(query=None,
                    path=response['nextRecordsUrl'])
        return response['records']

    def post(self, path=None, data=None):
        """
        Call the Salesforce API to make inserts/updates.
        """
        url = '{}{}'.format(self.instance_url, path)
        resp = requests.post(url, headers=self.headers, data=json.dumps(data))
        response = json.loads(resp.text)
        check_response(response=resp, expected_status=201)
        return response

    def _format_contact(self, form=None):
        """
        Format a contact for update/insert.
        """

        try:
            stripe_id = form['Stripe_Customer_Id__c']
        except KeyError:
            stripe_id = None

        contact = {
            'Email': form['stripeEmail'],
            'FirstName': form['first_name'],
            'LastName': form['last_name'],
            'Description': form['description'],
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
        response = self.query(query)
        # unlike elsewhere there should only be one result here because we're
        # querying on a 1:1 relationship:
        contact = response[0]
        return contact

    def create_contact(self, form):
        """
        Create and return a contact. Then fetch that created contact to get
        the associated account ID.
        """

        print ("----Creating contact...")
        contact = self._format_contact(form=form)
        path = '/services/data/v34.0/sobjects/Contact'
        response = self.post(path=path, data=contact)
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
        response = self.query(query)
        return response

    def get_or_create_contact(self, form):
        """
        Return a contact. If one already exists it's returned. Otherwise
        a new contact is created and returned.
        """

        created = False
        email = form['stripeEmail']

        response = self.find_contact(email=email)

        # if the response is empty then nothing matched and we
        # have to create a contact:
        if len(response) < 1:
            contact = self.create_contact(form)
            created = True
            return created, contact

        elif len(response) > 1:
            warn_multiple_accounts(email=email, count=len(response))

        return created, response[0]


def check_response(response=None, expected_status=200):
    """
    Check the response from API calls to determine if they succeeded and
    if not, why.
    """
    code = response.status_code
    try:
        content = json.loads(response.content.decode('utf-8'))
        # TODO: look for 'success'
        #print (content)
    except:
        print ('unable to parse response (this is probably okay)')
    if code != expected_status:
        print (content)
        raise Exception('Expected {} but got {}'.format(expected_status, code))
    return True


def upsert_customer(customer=None, form=None):
    """
    Creates the user if it doesn't exist in Salesforce. If it does exist
    the Stripe Customer ID is added to the Salesforce record.
    """

    if customer is None:
        raise Exception("Value for 'customer' must be specified.")
    if form is None:
        raise Exception("Value for 'form' must be specified.")

    update = {'Stripe_Customer_Id__c': customer.id}
    updated_request = update.copy()
    updated_request.update(form.to_dict())

    sf = SalesforceConnection()
    created, contact = sf.get_or_create_contact(updated_request)

    if not created:
        print ("----Exists, updating")

        path = '/services/data/v34.0/sobjects/Contact/{}'.format(contact['Id'])
        url = '{}{}'.format(sf.instance_url, path)
        resp = requests.patch(url, headers=sf.headers, data=json.dumps(update))
        check_response(response=resp, expected_status=204)

    return True


def _format_opportunity(contact=None, form=None, customer=None):
    """
    Format an opportunity for insertion.
    """

    today = datetime.now(tz=zone).strftime('%Y-%m-%d')

    if form['pay_fees_value'] == 'True':
        pay_fees = True
    else:
        pay_fees = False

    opportunity = {
            'AccountId': '{}'.format(contact['AccountId']),
            'Amount': '{}'.format(form['amount']),
            'CloseDate': today,
            'RecordTypeId': DONATION_RECORDTYPEID,
            'Name': '{}{} ({})'.format(
                form['first_name'],
                form['last_name'],
                form['stripeEmail'],
                ),
            'StageName': 'Pledged',
            'Stripe_Customer_Id__c': customer.id,
            'LeadSource': 'Stripe',
            'Description': '{}'.format(form['description']),
            'Stripe_Agreed_to_pay_fees__c': pay_fees,
            'Encouraged_to_contribute_by__c': '{}'.format(form['reason']),
            # Co Member First name, last name, and email
            }
    return opportunity


def add_opportunity(form=None, customer=None, charge=None):

    print ("----Adding opportunity...")
    sf = SalesforceConnection()
    _, contact = sf.get_or_create_contact(form)
    opportunity = _format_opportunity(contact=contact, form=form,
            customer=customer)
    path = '/services/data/v34.0/sobjects/Opportunity'
    response = sf.post(path=path, data=opportunity)
    send_multiple_account_warning()

    return response


def _format_recurring_donation(contact=None, form=None, customer=None):
    """
    Format a recurring donation for insertion into SF.
    """

    today = datetime.now(tz=zone).strftime('%Y-%m-%d')
    now = datetime.now(tz=zone).strftime('%Y-%m-%d %I:%M:%S %p %Z')
    amount = form['amount']
    type__c = ''
    try:
        installments = form['installments']
    except:
        installments = 'None'
    try:
        open_ended_status = form['openended_status']
    except:
        open_ended_status = 'None'
    try:
        installment_period = form['installment_period']
    except:
        installment_period = 'None'

    # TODO: test this
    if open_ended_status == 'None' and (
            installments == '3' or installments == '36') and (
                    installment_period == 'yearly' or
                    installment_period == 'monthly'):
        type__c = 'Giving Circle'

    # TODO: test this:
    if installments != 'None':
        amount = int(amount) * int(installments)
    else:
        installments = 0

    if form['pay_fees_value'] == 'True':
        pay_fees = True
    else:
        pay_fees = False

    recurring_donation = {
            'npe03__Contact__c': '{}'.format(contact['Id']),
            'npe03__Amount__c': '{}'.format(amount),
            'npe03__Date_Established__c': today,
            'npe03__Open_Ended_Status__c': '',
            'Name': '{} for {} {}'.format(
                now,
                form['first_name'],
                form['last_name'],
                ),
            'Stripe_Customer_Id__c': customer.id,
            'Lead_Source__c': 'Stripe',
            'Stripe_Description__c': '{}'.format(form['description']),
            'Stripe_Agreed_to_pay_fees__c': pay_fees,
            'Encouraged_to_contribute_by__c': '{}'.format(
                form['reason']),
            'npe03__Open_Ended_Status__c': open_ended_status,
            'npe03__Installments__c': installments,
            'npe03__Installment_Period__c': installment_period,
            'Type__c': type__c,
            }
    return recurring_donation


def add_recurring_donation(form=None, customer=None):
    """
    Insert a recurring donation into SF.
    """

    print ("----Adding recurring donation...")
    sf = SalesforceConnection()
    _, contact = sf.get_or_create_contact(form)
    recurring_donation = _format_recurring_donation(contact=contact,
            form=form, customer=customer)
    path = '/services/data/v34.0/sobjects/npe03__Recurring_Donation__c'
    sf.post(path=path, data=recurring_donation)
    send_multiple_account_warning()

    return True


@celery.task(name='salesforce.add_customer_and_charge')
def add_customer_and_charge(form=None, customer=None):
    """
    Add a contact and their donation into SF. This is done in the background
    because there are a lot of API calls and there's no point in making the
    payer wait for them.
    """
    amount = form['amount']
    name = '{} {}'.format(form['first_name'], form['last_name'])
    reason = form['reason']
    if reason != '':
        reason = ' (encouraged by {})'.format(reason)

    upsert_customer(form=form, customer=customer)

    if (form['installment_period'] == 'None'):
        print("----One time payment...")
        msg = '{} pledged ${}{}'.format(name, amount, reason)
        notify_slack(msg)
        add_opportunity(form=form, customer=customer)
    else:
        print("----Recurring payment...")
        msg = '{} pledged ${}{} [recurring]'.format(name, amount, reason)
        notify_slack(msg)
        add_recurring_donation(form=form, customer=customer)
    return True
