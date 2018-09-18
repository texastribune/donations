from datetime import datetime
import json
from pprint import pprint
from io import StringIO
import csv

from pytz import timezone
from salesforce import SalesforceConnection
from fuzzywuzzy import process

zone = timezone("US/Central")  # TODO read in

DEFAULT_RECORDTYPEID = "01216000001IhI9"  # TODO
SALESFORCE_API_VERSION = "v43.0"  # TODO
ORGANIZATION_RECORDTYPEID = '01216000001IhHMAA0' # TODO

# TODO use f-strings?
# TODO reuse save() methods?


class Opportunity(object):

    sf = SalesforceConnection()

    path = "/services/data/{}/sobjects/Opportunity/".format(SALESFORCE_API_VERSION)

    def __init__(self):

        today = datetime.now(tz=zone).strftime("%Y-%m-%d")

        self.id = None
        self.account_id = None
        self.amount = 0
        self.close_date = today
        self.campaign_id = None
        self.record_type_id = DEFAULT_RECORDTYPEID
        self.name = None
        self.stage_name = "Pledged"
        self.type = "Single"
        self.stripe_customer_id = None
        self.referral_id = None
        self.lead_source = None
        self.description = None
        self.agreed_to_pay_fees = False
        self.encouraged_by = None
        self.created = False

    def _format(self):
        opportunity = {
            "AccountId": "{}".format(self.account_id),
            "Amount": "{}".format(self.amount),
            "CloseDate": self.close_date,
            "Campaignid": self.campaign_id,
            "RecordTypeId": self.record_type_id,
            "Name": "{}".format(self.name),
            "StageName": "Pledged",
            "Type": "Single",
            "Stripe_Customer_Id__c": self.stripe_customer_id,
            "Referral_ID__c": self.referral_id,
            "LeadSource": "Stripe",
            "Description": "{}".format(self.description),
            "Stripe_Agreed_to_pay_fees__c": self.agreed_to_pay_fees,
            "Encouraged_to_contribute_by__c": "{}".format(self.encouraged_by),
        }
        print(opportunity)
        return opportunity

    def save(self):

        if self.account_id is None:
            # TODO: custom exception
            raise Exception("Account ID must be specified")
        if not self.name:
            raise Exception("Opportunity name must be specified")

        if self.id:
            print("already exists; updating...")
            try:
                path = self.path + "{}".format(self.id)
                print(path)
                response = self.sf.patch(path=path, data=self._format())
            except Exception as e:
                content = json.loads(e.response.content.decode("utf-8"))
                print(content)
                # TODO: same kind of referral ID/campaign ID handling here?
            return

        try:
            print(self.path)
            response = self.sf.post(path=self.path, data=self._format())
            print(response)
            self.id = response["id"]
            self.created = True
        except Exception as e:
            content = json.loads(e.response.content.decode("utf-8"))
            print(content)
            # retry without a campaign if it gives an error
            if "Campaign ID" in content[0]["message"]:
                print("bad campaign ID; retrying...")
                self.campaign_id = ""
                self.save()
            elif "Referral ID" in content[0]["message"]:
                print("bad referral ID; retrying...")
                self.referral_id = ""
                self.save()
            else:
                raise (e)

        return


class RDO(object):

    sf = SalesforceConnection()

    path = "/services/data/{}/sobjects/npe03__Recurring_Donation__c/".format(
        SALESFORCE_API_VERSION
    )

    def __init__(self):

        today = datetime.now(tz=zone).strftime("%Y-%m-%d")

        self.id = None
        self.installments = None
        self.open_ended_status = None
        self.installment_period = None
        self.campaign_id = None
        self.referral_id = None
        self.amount = 0
        self.type = "Recurring Donation"
        self.contact_id = None
        self.date_established = today
        self.name = ""
        self.stripe_customer_id = None
        self.lead_source = "Stripe"
        self.description = ""
        self.agreed_to_pay_fees = False
        self.encouraged_by = ""
        self.account_id = None
        self.created = False

    def _format(self):
        recurring_donation = {
            'npe03__Organization__c': self.account_id,
            "Referral_ID__c": self.referral_id,
            "npe03__Recurring_Donation_Campaign__c": self.campaign_id,
            "npe03__Contact__c": self.contact_id,
            "npe03__Amount__c": self.amount,
            "npe03__Date_Established__c": self.date_established,
            "Name": "".format(self.name),
            "Stripe_Customer_Id__c": self.stripe_customer_id,
            "Lead_Source__c": "{}".format(self.lead_source),
            "Stripe_Description__c": "{}".format(self.description),
            "Stripe_Agreed_to_pay_fees__c": self.agreed_to_pay_fees,
            "Encouraged_to_contribute_by__c": "{}".format(self.encouraged_by),
            "npe03__Open_Ended_Status__c": self.open_ended_status,
            "npe03__Installments__c": self.installments,
            "npe03__Installment_Period__c": self.installment_period,
            "Type__c": self.type,
        }
        pprint(recurring_donation)  # TODO: rm
        return recurring_donation

    def save(self):

        if self.account_id is None and self.contact_id is None:
            raise Exception("One of Contact ID or Account ID must be specified.")

        if self.id:
            print("already exists; updating...")
            try:
                path = self.path + "{}".format(self.id)
                print(path)
                response = self.sf.patch(path=path, data=self._format())
            except Exception as e:
                content = json.loads(e.response.content.decode("utf-8"))
                print(content)
                # TODO: same kind of referral ID/campaign ID handling here?
            return

        try:
            print(self.path)
            response = self.sf.post(path=self.path, data=self._format())
            print(response)
            self.id = response["id"]
            self.created = True
        except Exception as e:
            content = json.loads(e.response.content.decode("utf-8"))
            print(content)
            # retry without a campaign if it gives an error
            if "Campaign ID" in content[0]["message"]:
                print("bad campaign ID; retrying...")
                self.campaign_id = ""
                self.save()
            elif "Referral ID" in content[0]["message"]:
                print("bad referral ID; retrying...")
                self.referral_id = ""
                self.save()
            else:
                raise (e)

        return


class Account(object):

    sf = SalesforceConnection()

    path = "/services/data/{}/sobjects/Account/".format(SALESFORCE_API_VERSION)

    def __init__(self):

        self.id = None
        self.name = None
        self.created = False
        self.website = None

    def _format(self):
        account = {
            'Id': '{}'.format(self.id),
            'Website': '{}'.format(self.website),
            'RecordTypeId': ORGANIZATION_RECORDTYPEID,
            "Name": "{}".format(self.name),
        }
        pprint(account)  # TODO: rm
        return account

    def __str__(self):
        return json.dumps(self._format())

    @classmethod
    def get(cls, name=None, website=None):

        query = """
            SELECT Id, Name, Website
            FROM Account WHERE
            RecordTypeId = '{}'
        """.format(ORGANIZATION_RECORDTYPEID)

        response = cls.sf.query(query)
        pprint(response)
        website_idx = {x['Website']: {'id': x['Id'], 'name': x['Name']} for x in
                response if x['Website'] is not None
                and x['Website'] != 'NULL'}
        pprint(website_idx)
        url_list = list(website_idx.keys())

        extracted = process.extractOne(website, url_list)
        pprint(extracted)
        if extracted is None:
            return None
        url, confidence = extracted
        if confidence < 95:
            return None
        account = Account()
        account.id = website_idx[url]['id']
        account.name = website_idx[url]['name']
        account.website = url
        return account

    def save(self):

        if self.id:
            print("already exists; updating...")
            try:
                path = self.path + "{}".format(self.id)
                print(path)
                response = self.sf.patch(path=path, data=self._format())
            except Exception as e:
                content = json.loads(e.response.content.decode("utf-8"))
                print(content)
            return

        try:
            print(self.path)
            response = self.sf.post(path=self.path, data=self._format())
            print(response)
            self.id = response["id"]
            self.created = True
        except Exception as e:
            content = json.loads(e.response.content.decode("utf-8"))
            print(content)
            raise (e)

        return

class Contact(object):

    sf = SalesforceConnection()

    path = "/services/data/{}/sobjects/Account/".format(SALESFORCE_API_VERSION)

    def __init__(self):
        self.id = None
        self.account_id = None
        self.first_name = None
        self.last_name = None
        self.created = False
        self.email = None
        self.lead_source = None
        self.mailing_postal_code = None
        self.duplicate_found = False

    @staticmethod
    def parse_all_email(email=None, input=None):
        results = list()
        for item in input:
            all_email = item['All_In_One_EMail__c']
            buffer = StringIO(all_email)
            reader = csv.reader(buffer)
            if email in list(reader)[0]:
                print ('email in list')
                results.append(item)
        return results

    def _format(self):
        contact = {
            'Id': self.id,
            'Email': self.email,
            'FirstName': self.first_name,
            'LastName': self.last_name,
            'LeadSource': self.lead_source,
            'MailingPostalCode': self.mailing_postal_code,
            }
        print(contact)
        return contact

    def __str__(self):
        return json.dumps(self._format())

    @classmethod
    def get(cls, id=None, email=None):

        if id is None and email is None:
            raise Exception('id or email must be specified')
        if id and email:
            raise Exception("id and email can't both be specified")
        if id:
            query = """
                    SELECT Id, AccountId, FirstName, LastName, LeadSource, Stripe_Customer_Id__c, MailingPostalCode, Email
                    FROM Contact
                    WHERE id = '{}'
                    """.format(id)
            response = cls.sf.query(query)
            # should only be one result here because we're
            # querying on a 1:1 relationship:
            response = response[0]
            # TODO exception if it's not found?
            contact = Contact()
            contact.id = response['Id']
            contact.account_id = response['AccountId']
            contact.first_name = response['FirstName']
            contact.last_name = response['LastName']
            contact.email = response['Email']
            contact.lead_source = response['LeadSource']
            contact.mailing_postal_code = response['MailingPostalCode']
            return contact

        query = """
                SELECT Id, AccountId, FirstName, LastName, LeadSource, MailingPostalCode, All_In_One_EMail__c, Email
                FROM Contact
                WHERE All_In_One_EMail__c
                LIKE '%{}%'
                """.format(email)
        pprint(query)
        response = cls.sf.query(query)
        pprint(response)
        if len(response) == 0:
            return None
        response = cls.parse_all_email(email=email, input=response)
        pprint(response)
        if len(response) == 0:
            return None
        contact = Contact()
        if len(response) > 1:
            contact.duplicate_found = True
        response = response[0]
        contact.id = response['Id']
        contact.account_id = response['AccountId']
        contact.first_name = response['FirstName']
        contact.last_name = response['LastName']
        contact.email = response['Email']
        contact.lead_source = response['LeadSource']
        contact.mailing_postal_code = response['MailingPostalCode']

        return contact

    def save(self):

        if self.id:
            print("already exists; updating...")
            try:
                path = self.path + "{}".format(self.id)
                print(path)
                response = self.sf.patch(path=path, data=self._format())
            except Exception as e:
                content = json.loads(e.response.content.decode("utf-8"))
                print(content)
            return

        try:
            print(self.path)
            response = self.sf.post(path=self.path, data=self._format())
            print(response)
            self.id = response["id"]
            self.created = True
        except Exception as e:
            content = json.loads(e.response.content.decode("utf-8"))
            print(content)
            raise (e)

        return
