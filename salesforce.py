from datetime import datetime
from decimal import Decimal
import json
import locale
from pprint import pprint   # TODO: remove

import celery
import requests
from pytz import timezone
import stripe

from config import SALESFORCE
from config import DONATION_RECORDTYPEID
from config import TIMEZONE
from config import ENABLE_SLACK
from config import SLACK_API_KEY
from config import SLACK_CHANNEL
from config import MULTIPLE_ACCOUNT_WARNING_MAIL_RECIPIENT

from emails import send_email
from check_response import check_response

zone = timezone(TIMEZONE)

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

TWOPLACES = Decimal(10) ** -2       # same as Decimal('0.01')

WARNINGS = dict()

#TODO see if there's already an opportunity on that date with that amount and warn/skip if so
#TODO using logging instead of print()


def notify_slack(message):
    """
    Send a notification about a donation to Slack.
    """
    if ENABLE_SLACK:
        payload = {
                'token': SLACK_API_KEY,
                'channel': SLACK_CHANNEL,
                'text': message,
                'username': 'moneybot',
                'icon_emoji': ':moneybag:'

                }
        url = 'https://slack.com/api/chat.postMessage'
        try:
            requests.get(url, params=payload)
        except Exception as e:
            print('Failed to send Slack notification: {}'.format(e))


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
    print('send_multiple_account_warning called...')

    for email in list(WARNINGS.keys()):
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
                recipient=MULTIPLE_ACCOUNT_WARNING_MAIL_RECIPIENT,
                subject='Multiple accounts found for {}'.format(email),
                body=body
                )

        del WARNINGS[email]


def get_email(form):
    if 'subscriber_email' in form:
        email = form['subscriber_email']
        print('found subscriber email: {}'.format(email))
        return email
    else:
        return form.get('stripeEmail')


def _format_contact(form=None):
    """
    Format a contact for update/insert.
    """

    email = get_email(form)

    stripe_id = form.get('Stripe_Customer_Id__c', None)

    zipcode = form.get('zipcode', None)

    contact = {
        'Email': email,
        'FirstName': form['first_name'],
        'LastName': form['last_name'],
        'Description': form['description'],
        'LeadSource': 'Stripe',
        'Stripe_Customer_Id__c': stripe_id,
        'MailingPostalCode': zipcode,
        }
    print(contact)
    return contact


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

    def query(self, query, path='/services/data/v35.0/query'):
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

    def patch(self, path=None, data=None):
        """
        Call the Saleforce API to make PATCH requests
        """

        url = '{}{}'.format(self.instance_url, path)
        resp = requests.patch(url, headers=self.headers,
            data=json.dumps(data))
        check_response(response=resp, expected_status=204)
        return resp

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

        print('----Creating contact...')
        contact = _format_contact(form=form)
        path = '/services/data/v35.0/sobjects/Contact'
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
        email = get_email(form)

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


def _format_amount(number):
    return str(Decimal(number).quantize(TWOPLACES))


def upsert_customer(customer=None, form=None):
    """
    Creates the user if it doesn't exist in Salesforce. If it does exist
    the Stripe Customer ID is added to the Salesforce record.
    """

    if customer is None:
        raise Exception('Value for "customer" must be specified.')
    if form is None:
        raise Exception('Value for "form" must be specified.')

    pprint('form: {}'.format(form))

    update = {'Stripe_Customer_Id__c': customer.id}

    if 'zipcode' in form and form['zipcode'] not in [None, '']:
        update['MailingPostalCode'] = form['zipcode']

    pprint('update: {}'.format(update))

    updated_request = update.copy()
    updated_request.update(form.to_dict())

    pprint('updated_request: {}'.format(updated_request))

    sf = SalesforceConnection()
    created, contact = sf.get_or_create_contact(updated_request)

    if not created:
        print('----Exists, updating')

        #TODO: why not use sf.patch()?

        path = '/services/data/v35.0/sobjects/Contact/{}'.format(contact['Id'])
        url = '{}{}'.format(sf.instance_url, path)
        resp = requests.patch(url, headers=sf.headers, data=json.dumps(update))
        print(resp)
        check_response(response=resp, expected_status=204)

    return True


def _format_opportunity(contact=None, form=None, customer=None, date=None, stage='Closed Won'):
    """
    Format an opportunity for insertion.
    """
    if date is None:
        date = datetime.now(tz=zone).strftime('%Y-%m-%d')

    campaign_id = form.get('campaign_id', default='')
    pay_fees = form['pay_fees_value'] == 'True'
    amount = _format_amount(form['amount'])

    opportunity = {
            'AccountId': '{}'.format(contact['AccountId']),
            'Amount': '{}'.format(amount),
            'CloseDate': date,
            'Campaignid': campaign_id,
            'RecordTypeId': DONATION_RECORDTYPEID,
            'Name': '{} {} ({})'.format(
                form['first_name'],
                form['last_name'],
                form['stripeEmail'],
                ),
            'Type': 'Single',
            'Stripe_Customer_Id__c': customer.id,
            'LeadSource': 'Stripe',
            'Description': '{}'.format(form['description']),
            'Stripe_Agreed_to_pay_fees__c': pay_fees,
            'Encouraged_to_contribute_by__c': '{}'.format(form['reason']),
            'StageName': stage,
            }

    pprint(opportunity)
    return opportunity


def _amount_to_charge(amount, pay_fees=False):
    """
    determine the amount to charge. this depends on whether the payer agreed
    to pay fees or not. if they did then we add that to the amount charged.
    stripe charges 2.2% + $0.30.

    stripe wants the amount to charge in cents. so we multiply by 100 and
    return that.

    https://support.stripe.com/questions/can-i-charge-my-stripe-fees-to-my-customers
    """
    amount = float(amount)

    if pay_fees:
        total = (amount + .30) / (1 - 0.022)
    else:
        total = amount
    total_in_cents = total * 100

    return int(total_in_cents)


def update_opportunity(opp_id, card_id=None, txn_id=None, referral_id=None, stage=None):

    print('Updating Opportunity ({})...'.format(opp_id))
    sf = SalesforceConnection()
    print(opp_id)

    update = dict()
    if stage:
        update['StageName'] = stage
    if txn_id:
        update['Stripe_Transaction_Id__c'] = txn_id
    if card_id:
        update['Stripe_Card__c'] = card_id
    if referral_id:
        update['Referral_ID__c'] = referral_id
    print(update)
    path = '/services/data/v35.0/sobjects/Opportunity/{}'.format(opp_id)
    sf.patch(path, update)


def _check_duplicate_opportunity(account_id, opp_type='Single', date=None):

    print('Checking for duplicate transactions...')
    if date is None:
        date = datetime.now(tz=zone).strftime('%Y-%m-%d')

    query = """
        SELECT Id FROM Opportunity
        WHERE AccountId = '{}'
        AND Type = '{}'
        AND CloseDate = {}
    """.format(account_id, opp_type, date)

    print(query)
    sf = SalesforceConnection()
    response = sf.query(query)
    print(response)

# TODO:
    if len(response) != 0:
        raise Exception('Possible duplicate transaction. Not charging.')
    return response


def add_opportunity(form=None, customer=None):

    print('----Adding opportunity...')

    pay_fees = form['pay_fees_value'] == 'True'
    amount = _amount_to_charge(form['amount'], pay_fees)

    sf = SalesforceConnection()
    _, contact = sf.get_or_create_contact(form)

    response = _check_duplicate_opportunity(account_id=contact['AccountId'])

    opportunity = _format_opportunity(contact=contact, form=form,
            customer=customer)
    path = '/services/data/v35.0/sobjects/Opportunity'
    try:
        response = sf.post(path=path, data=opportunity)
        opp_id = response['id']
    except Exception as e:
        content = json.loads(e.response.content.decode('utf-8'))
        print(content)
        # retry without a campaign if it gives an error
        if 'Campaign ID' in content[0]['message']:
            print('bad campaign ID; retrying...')
            opportunity['Campaignid'] = ''
            response = sf.post(path=path, data=opportunity)
            opp_id = response['id']
        else:
            raise(e)

    if 'referral_id' in form:
        try:
            response = update_opportunity(opp_id=opp_id, referral_id=form['referral_id'])
        except Exception as e:
            content = json.loads(e.response.content.decode('utf-8'))
            print(content)
            print ('Unable to add referral ID: {}'.format(content[0]['message']))

    print('---- Charging ${} to {} ({} {})'.format(amount / 100,
        customer.id, form['first_name'],form['last_name']))

    charge = stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description=form['description'],
            )

    print(charge.outcome.seller_message)
    response = update_opportunity(opp_id=opp_id, card_id=charge.source.id,
            stage='Closed Won', txn_id=charge.id)

    print(response)
    send_multiple_account_warning()

    return


def _format_recurring_donation(contact=None, form=None, customer=None):
    """
    Format a recurring donation for insertion into SF.
    """

    today = datetime.now(tz=zone).strftime('%Y-%m-%d')
    now = datetime.now(tz=zone).strftime('%Y-%m-%d %I:%M:%S %p %Z')
    amount = form['amount']
    type__c = 'Recurring Donation'

    installments = form.get('installments', default='None')
    open_ended_status = form.get('openended_status', default='None')
    installment_period = form.get('installment_period', default='None')
    campaign_id = form.get('campaign_id', default='')
    referral_id = form.get('referral_id', default='')
    pay_fees = form['pay_fees_value'] == 'True'

    # TODO: test this
    if open_ended_status == 'None' and (
            installments == '3' or installments == '36') and (
                    installment_period == 'yearly' or
                    installment_period == 'monthly'):
        type__c = 'Giving Circle'

    # TODO: test this:
    if installments != 'None':
        amount = float(amount) * int(installments)
    else:
        installments = 0

    recurring_donation = {
            'npe03__Recurring_Donation_Campaign__c': campaign_id,
            'npe03__Contact__c': '{}'.format(contact['Id']),
            'npe03__Amount__c': '{}'.format(_format_amount(amount)),
            'npe03__Date_Established__c': today,
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
    pprint(recurring_donation)   # TODO: rm
    return recurring_donation

def get_rdo_opp(rdo_id):

    print('Finding first Opportunity for new RDO...')

    today = datetime.now(tz=zone).strftime('%Y-%m-%d')
    query = """
        SELECT Id, StageName FROM Opportunity
        WHERE npe03__Recurring_Donation__c = '{}'
        AND CloseDate = {}
    """.format(rdo_id, today)
    try:
        sf = SalesforceConnection()
        response = sf.query(query)
    except Exception as e:
        print(e.response.content.decode('utf-8'))
        raise(e)

    if len(response) != 1:
        raise Exception('More than one Opportunity found.')

    if response[0]['StageName'] != 'Pledged':
        raise Exception('Opportunity stage is not Pledged')

    return response[0]


#TODO consistent use of quotes

def update_rdo(rdo_id, referral_id=None):

    print('Updating RDO ({})...'.format(rdo_id))
    sf = SalesforceConnection()

    update = dict()
    if referral_id:
        update['Referral_ID__c'] = referral_id
    print(update)
    path = '/services/data/v35.0/sobjects/npe03__Recurring_Donation__c/{}'.format(rdo_id)
    sf.patch(path, update)


def add_recurring_donation(form=None, customer=None):
    """
    Insert a recurring donation into SF.
    """

    print('----Adding recurring donation...')
    sf = SalesforceConnection()
    _, contact = sf.get_or_create_contact(form)
    response = _check_duplicate_opportunity(opp_type='Recurring Donation',
            account_id=contact['AccountId'])
    recurring_donation = _format_recurring_donation(contact=contact,
            form=form, customer=customer)
    path = '/services/data/v35.0/sobjects/npe03__Recurring_Donation__c'
    try:
        response = sf.post(path=path, data=recurring_donation)
        print(response)
    except Exception as e:
        content = json.loads(e.response.content.decode('utf-8'))
        # retry without a campaign if it gives an error
        if 'Campaign: id' in content[0]['message']:
            print('bad campaign ID; retrying...')
            recurring_donation['npe03__Recurring_Donation_Campaign__c'] = ''
            response = sf.post(path=path, data=recurring_donation)
        else:
            raise(e)

    rdo_id = response['id']

    if 'referral_id' in form:
        try:
            response = update_rdo(rdo_id=rdo_id, referral_id=form['referral_id'])
        except Exception as e:
            content = json.loads(e.response.content.decode('utf-8'))
            print(content)
            print ('Unable to add referral ID: {}'.format(content[0]['message']))

    response = get_rdo_opp(rdo_id)
    opp_id = response['Id']
    response = update_opportunity(opp_id, stage='Closed Won')
    print(response)

    print('Charging card...')

    pay_fees = form['pay_fees_value'] == 'True'
    amount = _amount_to_charge(form['amount'], pay_fees)

    #TODO catch charge failures and mark them in SF

    charge = stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description=form['description'],
            )

    print(charge.outcome.seller_message)
    response = update_opportunity(opp_id=opp_id, card_id=charge.source.id,
            stage='Closed Won', txn_id=charge.id)

    print(response)

    #TODO look for Closed Won opportunities that don't have Stripe details

    send_multiple_account_warning()

    return True


@celery.task(name='salesforce.add_customer_and_charge')
def add_customer_and_charge(form=None, customer=None):
    """
    Add a contact and their donation into SF. This is done in the background
    because there are a lot of API calls and there's no point in making the
    payer wait for them.
    """
    amount = _format_amount(form['amount'])
    name = '{} {}'.format(form['first_name'], form['last_name'])
    reason = form['reason']
    period = form['installment_period']
    email = form['stripeEmail']
    if reason != '':
        reason = ' (encouraged by {})'.format(reason)

    upsert_customer(form=form, customer=customer)

    if (form['installment_period'] == 'None'):
        print('----One time payment...')
        msg = '*{}* ({}) pledged *${}*{}'.format(name, email, amount, reason)
        notify_slack(msg)
        add_opportunity(form=form, customer=customer)
    else:
        print('----Recurring payment...')
        msg = '*{}* ({}) pledged *${}*{} [{}]'.format(name, email, amount,
                reason, period)
        notify_slack(msg)
        add_recurring_donation(form=form, customer=customer)
    return True


def _format_blast_rdo(contact=None, form=None, customer=None):
    """
    Format a Blast subscription for insertion into SF.
    """

    today = datetime.now(tz=zone).strftime('%Y-%m-%d')
    now = datetime.now(tz=zone).strftime('%Y-%m-%d %I:%M:%S %p %Z')
    amount = form['amount']
    installments = 0
    open_ended_status = 'Open'
    pay_fees = form['pay_fees_value'] == 'True'

    if amount == '40':
        installment_period = 'monthly'
    else:
        installment_period = 'yearly'

    campaign_id = form.get('campaign_id', default='')
    referral_id = form.get('referral_id', default='')

    blast_subscription = {
            'npe03__Recurring_Donation_Campaign__c': campaign_id,
            'npe03__Contact__c': '{}'.format(contact['Id']),
            'npe03__Amount__c': '{}'.format(amount),
            'npe03__Date_Established__c': today,
            'Name': '{} {} - {} - The Blast'.format(
                form['first_name'],
                form['last_name'],
                now,
                ),
            'Stripe_Customer_Id__c': customer.id,
            'Lead_Source__c': 'Stripe',
            'Stripe_Description__c': '{}'.format(form['description']),
            'Stripe_Agreed_to_pay_fees__c': pay_fees,
            'npe03__Open_Ended_Status__c': open_ended_status,
            'npe03__Installments__c': installments,
            'npe03__Installment_Period__c': installment_period,
            'Type__c': 'The Blast',
            'Billing_Email__c': '{}'.format(form['stripeEmail']),
            'Blast_Subscription_Email__c': '{}'.format(
                form['subscriber_email']),
            }
    pprint(blast_subscription)   # TODO: rm
    return blast_subscription


def add_blast_subscription(form=None, customer=None, charge=None):

    print('----Adding Blast RDO...')

    pay_fees = form['pay_fees_value'] == 'True'
    amount = _amount_to_charge(form['amount'], pay_fees)

    sf = SalesforceConnection()
    _, contact = sf.get_or_create_contact(form)

    response = _check_duplicate_opportunity(opp_type='The Blast',
            account_id=contact['AccountId'])

    recurring_donation = _format_blast_rdo(contact=contact,
            form=form, customer=customer)
    path = '/services/data/v35.0/sobjects/npe03__Recurring_Donation__c'
    try:
        response = sf.post(path=path, data=recurring_donation)
    except Exception as e:
        content = json.loads(e.response.content.decode('utf-8'))
        # retry without a campaign if it gives an error
        if 'Campaign: id' in content[0]['message']:
            print('bad campaign ID; retrying...')
            recurring_donation['npe03__Recurring_Donation_Campaign__c'] = ''
            response = sf.post(path=path, data=recurring_donation)
            pprint(response)
        else:
            raise(e)

    rdo_id = response['id']
    if 'referral_id' in form:
        try:
            response = update_rdo(rdo_id=rdo_id, referral_id=form['referral_id'])
        except Exception as e:
            content = json.loads(e.response.content.decode('utf-8'))
            print(content)
            print ('Unable to add referral ID: {}'.format(content[0]['message']))

    response = get_rdo_opp(rdo_id)
    opp_id = response['Id']

    response = update_opportunity(opp_id, stage='Closed Won')
    print(response)

    print('---- Charging ${} to {} ({} {})'.format(amount / 100,
        customer.id, form['first_name'],form['last_name']))

    charge = stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description=form['description'],
            )
    print(charge.outcome.seller_message)

    response = update_opportunity(opp_id=opp_id, card_id=charge.source.id,
            stage='Closed Won', txn_id=charge.id)

    print(response)

    send_multiple_account_warning()

    return response


@celery.task(name='salesforce.add_blast_customer_and_charge')
def add_blast_customer_and_charge(form=None, customer=None):

    upsert_customer(customer=customer, form=form)

    add_blast_subscription(form=form, customer=customer)

    return True
