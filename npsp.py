import csv
import json
import logging
import os
from datetime import datetime
from decimal import Decimal
from io import StringIO

import requests
from fuzzywuzzy import process
from pytz import timezone
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

ZONE = timezone(os.environ.get("TIMEZONE", "US/Central"))

SALESFORCE_API_VERSION = os.environ.get("SALESFORCE_API_VERSION", "v43.0")

SALESFORCE_CLIENT_ID = os.environ.get("SALESFORCE_CLIENT_ID", "")
SALESFORCE_CLIENT_SECRET = os.environ.get("SALESFORCE_CLIENT_SECRET", "")
SALESFORCE_USERNAME = os.environ.get("SALESFORCE_USERNAME", "")
SALESFORCE_PASSWORD = os.environ.get("SALESFORCE_PASSWORD", "")
SALESFORCE_HOST = os.environ.get("SALESFORCE_HOST", "")

TWOPLACES = Decimal(10) ** -2  # same as Decimal('0.01')

# this should match whatever record type Salesforce's NPSP is
# configured to use for opportunities on an RDO
DEFAULT_RDO_TYPE = os.environ.get("DEFAULT_RDO_TYPE", "Membership")

logging.getLogger("urllib3").setLevel(logging.DEBUG)


class SalesforceException(Exception):
    pass


def requests_retry_session(
    retries=3,
    backoff_factor=1,
    status_forcelist=(400, 500, 502, 503, 504),
    method_whitelist=False,
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        status=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        method_whitelist=method_whitelist,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


class SalesforceConnection(object):

    """
    Represents the Salesforce API.
    """

    host = SALESFORCE_HOST

    def __init__(self):

        self.payload = {
            "grant_type": "password",
            "client_id": SALESFORCE_CLIENT_ID,
            "client_secret": SALESFORCE_CLIENT_SECRET,
            "username": SALESFORCE_USERNAME,
            "password": SALESFORCE_PASSWORD,
        }
        token_path = "/services/oauth2/token"
        self.url = f"https://{self.host}{token_path}"

        self._instance_url = None

    def _get_token(self):

        r = requests_retry_session().post(self.url, data=self.payload)
        self.check_response(r)
        response = json.loads(r.text)

        self._instance_url = response["instance_url"]
        access_token = response["access_token"]

        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "X-PrettyPrint": "1",
            "Content-Type": "application/json",
        }

    @property
    def instance_url(self):
        if not self._instance_url:
            self._get_token()
        return self._instance_url

    @staticmethod
    def check_response(response=None, expected_status=200):
        """
        Check the response from API calls to determine if they succeeded and
        if not, why.
        """
        code = response.status_code
        if code == 204 and expected_status == 204:
            return True
        try:
            content = json.loads(response.content.decode("utf-8"))
        except Exception as e:
            logging.debug(f"Exception in check_response: {e}")
        if code != expected_status:
            e = SalesforceException(f"Expected {expected_status} but got {code}")
            try:
                e.content = content[0]
            except NameError:
                e.content = None
            except KeyError:
                e.content = content
            e.response = response
            logging.info(f"response.text: {response.text}")
            raise e
        return True

    def query(self, query, path=None):

        """
        Call the Salesforce API to do SOQL queries.
        """
        if path is None:
            path = f"/services/data/{SALESFORCE_API_VERSION}/query"

        url = f"{self.instance_url}{path}"
        if query is None:
            payload = {}
        else:
            payload = {"q": query}
        logging.debug(query)
        r = requests.get(url, headers=self.headers, params=payload)
        self.check_response(r)
        response = json.loads(r.text)
        # recursively get the rest of the records:
        if response["done"] is False:
            return response["records"] + self.query(
                query=None, path=response["nextRecordsUrl"]
            )
        logging.debug(response)
        return response["records"]

    def post(self, path, data):
        """
        Call the Salesforce API to make inserts.
        """
        url = f"{self.instance_url}{path}"
        resp = requests.post(url, headers=self.headers, data=json.dumps(data))
        response = json.loads(resp.text)
        self.check_response(response=resp, expected_status=201)
        logging.debug(response)
        return response

    def patch(self, path, data, expected_response=204):
        """
        Call the Saleforce API to make updates.
        """

        url = f"{self.instance_url}{path}"
        logging.debug(data)
        resp = requests.patch(url, headers=self.headers, data=json.dumps(data))
        self.check_response(response=resp, expected_status=expected_response)
        return resp

    def updates(self, objects, changes):

        if not objects:
            raise SalesforceException("at least one object must be specified")

        data = dict()
        # what should this value be?
        data["allOrNone"] = False
        records = list()
        for item in objects:
            record = dict()
            record["attributes"] = {"type": item.api_name}
            record["id"] = item.id
            for k, v in changes.items():
                record[k] = v
            records.append(record)
        data["records"] = records
        path = f"/services/data/{SALESFORCE_API_VERSION}/composite/sobjects/"
        response = self.patch(path, data, expected_response=200)
        response = json.loads(response.text)
        logging.debug(response)
        error = False
        for item in response:
            if item["success"] is not True:
                logging.warning(f"{item['errors']}")
                error = item["errors"]
        if error:
            raise SalesforceException(f"Failure on update: {error}")

        return response

    def save(self, sf_object):

        if sf_object.id:
            logging.info(f"{sf_object.api_name} object already exists; updating...")
            path = f"/services/data/{SALESFORCE_API_VERSION}/sobjects/{sf_object.api_name}/{sf_object.id}"
            try:
                response = self.patch(path=path, data=sf_object._format())
            except SalesforceException as e:
                logging.error(e.response.text)
                raise
            return sf_object

        logging.info(f"{sf_object.api_name} object doesn't exist; creating...")
        path = f"/services/data/{SALESFORCE_API_VERSION}/sobjects/{sf_object.api_name}"
        logging.debug(repr(sf_object))
        try:
            response = self.post(path=path, data=sf_object._format())
        except SalesforceException as e:
            logging.error(e.response.text)
            raise

        sf_object.id = response["id"]
        sf_object.created = True

        return sf_object


class SalesforceObject(object):
    """
    This is the parent of all the other Salesforce objects.
    """

    def _format(self):
        raise NotImplementedError

    def __repr__(self):
        obj = self._format()
        obj["Id"] = self.id
        return json.dumps(obj)

    def __init__(self, sf_connection=None):
        self.id = None
        self.sf = SalesforceConnection() if sf_connection is None else sf_connection


class Opportunity(SalesforceObject):

    api_name = "Opportunity"

    def __init__(
        self,
        record_type_name="Membership",
        contact=None,
        stage_name="Pledged",
        account=None,
        sf_connection=None,
    ):
        super().__init__(sf_connection)

        if contact and account:
            raise SalesforceException("Account and Contact can't both be specified")

        today = datetime.now(tz=ZONE).strftime("%Y-%m-%d")

        if account is not None:
            self.account_id = account.id
            self.name = None
        elif contact is not None:
            self.account_id = contact.account_id
            self.name = f"{contact.first_name} {contact.last_name} ({contact.email})"
        else:
            self.name = None
            self.account_id = None

        self.id = None
        self._amount = 0
        self._net_amount = 0
        self.donor_selected_amount = 0
        self.close_date = today
        self.campaign_id = None
        self.record_type_name = record_type_name
        self.stage_name = stage_name
        self.type = "Single"
        self.stripe_customer = None
        self.referral_id = None
        self.lead_source = None
        self.description = None
        self.agreed_to_pay_fees = False
        self.encouraged_by = None
        self.stripe_card = None
        self.stripe_card_brand = None
        self.stripe_card_last_4 = None
        self.stripe_card_expiration = None
        self.stripe_transaction_id = None
        self.expected_giving_date = None
        self.closed_lost_reason = None
        self.amazon_order_id = None
        self.created = False

    @classmethod
    def list(
        cls,
        begin=None,
        end=None,
        stage_name="Pledged",
        stripe_customer_id=None,
        sf_connection=None,
    ):

        # TODO a more generic dserializing method
        # TODO allow filtering by anything that uses equality?

        sf = SalesforceConnection() if sf_connection is None else sf_connection

        if stripe_customer_id is None:
            where = f"""
            WHERE Expected_Giving_Date__c <= {end}
            AND Expected_Giving_Date__c >= {begin}
            AND StageName = '{stage_name}'
        """
        else:
            where = f"""
                WHERE Stripe_Customer_ID__c = '{stripe_customer_id}'
                AND StageName = '{stage_name}'
            """

        query = f"""
            SELECT
                Id,
                Amount,
                Net_Amount__c,
                Donor_Selected_Amount__c,
                Name,
                Stripe_Customer_ID__c,
                Description,
                Stripe_Agreed_to_pay_fees__c,
                CloseDate,
                CampaignId,
                RecordType.Name,
                Type,
                Referral_ID__c,
                LeadSource,
                Encouraged_to_contribute_by__c,
                Stripe_Transaction_ID__c,
                Stripe_Card__c,
                AccountId,
                npsp__Closed_Lost_Reason__c,
                Expected_Giving_Date__c,
                Stripe_Card_Brand__c,
                Stripe_Card_Expiration__c,
                Stripe_Card_Last_4__c,
                Amazon_Order_Id__c
            FROM Opportunity
            {where}
        """

        response = sf.query(query)
        logging.debug(response)

        results = list()
        for item in response:
            y = cls()
            y.id = item["Id"]
            y.name = item["Name"]
            y.amount = item["Amount"]
            y.net_amount = item["Net_Amount__c"]
            y.donor_selected_amount = item["Donor_Selected_Amount__c"]
            y.stripe_customer = item["Stripe_Customer_ID__c"]
            y.description = item["Description"]
            y.agreed_to_pay_fees = item["Stripe_Agreed_to_pay_fees__c"]
            y.stage_name = "Pledged"
            y.close_date = item["CloseDate"]
            y.record_type_name = item["RecordType"]["Name"]
            y.expected_giving_date = item["Expected_Giving_Date__c"]
            y.campaign_id = item["CampaignId"]
            y.type = item["Type"]
            y.referral_id = item["Referral_ID__c"]
            y.lead_source = item["LeadSource"]
            y.encouraged_by = item["Encouraged_to_contribute_by__c"]
            y.stripe_transaction_id = item["Stripe_Transaction_ID__c"]
            y.stripe_card = item["Stripe_Card__c"]
            y.account_id = item["AccountId"]
            y.closed_lost_reason = item["npsp__Closed_Lost_Reason__c"]
            y.stripe_card_brand = item["Stripe_Card_Brand__c"]
            y.stripe_card_expiration = item["Stripe_Card_Expiration__c"]
            y.stripe_card_last_4 = item["Stripe_Card_Last_4__c"]
            y.amazon_order_id = item["Amazon_Order_Id__c"]
            y.created = False
            results.append(y)

        return results

    @property
    def amount(self):
        return str(Decimal(self._amount).quantize(TWOPLACES))

    @amount.setter
    def amount(self, amount):
        self._amount = amount

    @property
    def net_amount(self):
        net_amount = self._net_amount
        if not self._net_amount:
            net_amount = 0.0
        return str(Decimal(net_amount).quantize(TWOPLACES))

    @net_amount.setter
    def net_amount(self, net_amount):
        self._net_amount = net_amount

    def _format(self):
        return {
            "AccountId": self.account_id,
            "Amount": self.amount,
            "Net_Amount__c": self.net_amount,
            "Donor_Selected_Amount__c": self.donor_selected_amount,
            "CloseDate": self.close_date,
            "CampaignId": self.campaign_id,
            "RecordType": {"Name": self.record_type_name},
            "Name": self.name,
            "StageName": self.stage_name,
            "Type": self.type,
            "Stripe_Customer_ID__c": self.stripe_customer,
            "Referral_ID__c": self.referral_id,
            "LeadSource": self.lead_source,
            "Description": self.description,
            "Stripe_Agreed_to_pay_fees__c": self.agreed_to_pay_fees,
            "Encouraged_to_contribute_by__c": self.encouraged_by,
            "Stripe_Transaction_ID__c": self.stripe_transaction_id,
            "Stripe_Card__c": self.stripe_card,
            "npsp__Closed_Lost_Reason__c": self.closed_lost_reason,
            "Stripe_Card_Brand__c": self.stripe_card_brand,
            "Stripe_Card_Expiration__c": self.stripe_card_expiration,
            "Stripe_Card_Last_4__c": self.stripe_card_last_4,
            "Amazon_Order_Id__c": self.amazon_order_id,
        }

    @classmethod
    def update_card(cls, opportunities, card_details, sf_connection=None):
        if not opportunities:
            raise SalesforceException("at least one Opportunity must be specified")
        sf = SalesforceConnection() if sf_connection is None else sf_connection
        return sf.updates(opportunities, card_details)

    def __str__(self):
        return f"{self.id}: {self.name} for {self.amount} ({self.description})"

    def save(self):

        # TODO this will fail if name hasn't been set
        # truncate to 80 chars:
        self.name = self.name[:80]

        if self.account_id is None:
            raise SalesforceException("Account ID must be specified")
        if not self.name:
            raise SalesforceException("Opportunity name must be specified")

        try:
            self.sf.save(self)
            # TODO should the client decide what's retryable?
        except SalesforceException as e:
            if e.content["errorCode"] == "MALFORMED_ID":
                if e.content["fields"][0] == "CampaignId":
                    logging.warning("bad campaign ID; retrying...")
                    self.campaign_id = None
                    self.save()
                elif e.content["fields"][0] == "Referral_ID__c":
                    logging.warning("bad referral ID; retrying...")
                    self.referral_id = None
                    self.save()
                else:
                    raise
            else:
                raise


class RDO(SalesforceObject):
    """
    Recurring Donation objects.
    """

    api_name = "npe03__Recurring_Donation__c"

    def __init__(self, id=None, contact=None, account=None, sf_connection=None):
        super().__init__(sf_connection=sf_connection)

        if account and contact:
            raise SalesforceException("Account and Contact can't both be specified")

        today = datetime.now(tz=ZONE).strftime("%Y-%m-%d")

        if contact is not None:
            self.contact_id = contact.id
            self.name = f"{today} for {contact.first_name} {contact.last_name} ({contact.email})"
            self.account_id = None
        elif account is not None:
            self.account_id = account.id
            self.name = None
            self.contact_id = None
        else:
            self.name = None
            self.account_id = None
            self.contact_id = None

        self.id = id
        self.installments = None
        self.open_ended_status = None
        self.installment_period = None
        self.campaign_id = None
        self.referral_id = None
        self._amount = 0
        self.type = "Recurring Donation"
        self.date_established = today
        self.stripe_customer = None
        self.lead_source = None
        self.description = None
        self.agreed_to_pay_fees = False
        self.encouraged_by = None
        self.blast_subscription_email = None
        self.billing_email = None
        self.record_type_name = None

        self.stripe_card_brand = None
        self.stripe_card_expiration = None
        self.stripe_card_last_4 = None

        self.created = False

    def _format(self):

        # TODO be sure to reverse this on deserialization
        amount = self.amount

        # TODO should this be in the client?
        if self.installments:
            amount = str(float(self.amount) * int(self.installments))

        recurring_donation = {
            "npe03__Organization__c": self.account_id,
            "Referral_ID__c": self.referral_id,
            "npe03__Recurring_Donation_Campaign__c": self.campaign_id,
            "npe03__Contact__c": self.contact_id,
            "npe03__Amount__c": amount,
            "npe03__Date_Established__c": self.date_established,
            "Name": self.name,
            "Stripe_Customer_ID__c": self.stripe_customer,
            "Lead_Source__c": self.lead_source,
            "Stripe_Description__c": self.description,
            "Stripe_Agreed_to_pay_fees__c": self.agreed_to_pay_fees,
            "Encouraged_to_contribute_by__c": self.encouraged_by,
            "npe03__Open_Ended_Status__c": self.open_ended_status,
            "npe03__Installments__c": self.installments,
            "npe03__Installment_Period__c": self.installment_period,
            "Blast_Subscription_Email__c": self.blast_subscription_email,
            "Billing_Email__c": self.billing_email,
            "Type__c": self.type,
            "Stripe_Card_Brand__c": self.stripe_card_brand,
            "Stripe_Card_Expiration__c": self.stripe_card_expiration,
            "Stripe_Card_Last_4__c": self.stripe_card_last_4,
        }
        return recurring_donation

    def __str__(self):
        return f"{self.id}: {self.name} for {self.amount} ({self.description})"

    # TODO sensible way to cache this to prevent it from being run multiple times when nothing
    # has changed? The opportunities themselves may've changed even when the RDO hasn't so
    # this may not be doable.

    def opportunities(self):
        query = f"""
            SELECT Id, Amount, Name, Stripe_Customer_ID__c, Description,
            Stripe_Agreed_to_pay_fees__c, CloseDate, CampaignId,
            RecordType.Name, Type, Referral_ID__c, LeadSource,
            Encouraged_to_contribute_by__c, Stripe_Transaction_ID__c,
            Stripe_Card__c, AccountId, npsp__Closed_Lost_Reason__c,
            Expected_Giving_Date__c, Stripe_Card_Brand__c,
            Stripe_Card_Expiration__c, Stripe_Card_Last_4__c
            FROM Opportunity
            WHERE npe03__Recurring_Donation__c = '{self.id}'
        """
        # TODO must make this dynamic
        response = self.sf.query(query)
        results = list()
        for item in response:
            y = Opportunity(sf_connection=self.sf)
            y.id = item["Id"]
            y.name = item["Name"]
            y.amount = item["Amount"]
            y.stripe_customer = item["Stripe_Customer_ID__c"]
            y.description = item["Description"]
            y.agreed_to_pay_fees = item["Stripe_Agreed_to_pay_fees__c"]
            y.stage_name = "Pledged"
            y.close_date = item["CloseDate"]
            y.record_type_name = item["RecordType"]["Name"]
            y.expected_giving_date = item["Expected_Giving_Date__c"]
            y.campaign_id = item["CampaignId"]
            y.type = item["Type"]
            y.referral_id = item["Referral_ID__c"]
            y.lead_source = item["LeadSource"]
            y.encouraged_by = item["Encouraged_to_contribute_by__c"]
            y.stripe_transaction_id = item["Stripe_Transaction_ID__c"]
            y.stripe_card_brand = item["Stripe_Card_Brand__c"]
            y.stripe_card_expiration = item["Stripe_Card_Expiration__c"]
            y.stripe_card_last_4 = item["Stripe_Card_Last_4__c"]
            y.stripe_card = item["Stripe_Card__c"]
            y.account_id = item["AccountId"]
            y.closed_lost_reason = item["npsp__Closed_Lost_Reason__c"]
            y.created = False
            results.append(y)
        return results

    @property
    def amount(self):
        return str(Decimal(self._amount).quantize(TWOPLACES))

    @amount.setter
    def amount(self, amount):
        self._amount = amount

    def save(self):

        # truncate to 80 characters
        self.name = self.name[:80]

        if self.account_id is None and self.contact_id is None:
            raise SalesforceException(
                "One of Contact ID or Account ID must be specified."
            )

        try:
            self.sf.save(self)
        except SalesforceException as e:
            if e.content["errorCode"] == "MALFORMED_ID":
                if e.content["fields"][0] == "npe03__Recurring_Donation_Campaign__c":
                    logging.warning("bad campaign ID; retrying...")
                    self.campaign_id = None
                    self.save()
                elif e.content["fields"][0] == "Referral_ID__c":
                    logging.warning("bad referral ID; retrying...")
                    self.referral_id = None
                    self.save()
                else:
                    raise
            else:
                raise

        # since NPSP doesn't let you pass through the record
        # type ID of the opportunity (it will only use one hard-coded value)
        # we set them for all of the opportunities here. But if the RDO
        # is open ended then it'll create new opportunities of the wrong
        # type on its own. We warn about that.
        #
        # You should fix this through
        # process builder/mass action scheduler or some other process on the
        # SF side
        if self.record_type_name == DEFAULT_RDO_TYPE or self.record_type_name is None:
            return
        if self.open_ended_status == "Open":
            logging.warning(
                f"RDO {self} is open-ended so new opportunities won't have type {self.record_type_name}"
            )
            return
        logging.info(
            f"Setting record type for {self} opportunities to {self.record_type_name}"
        )
        update = {"RecordType": {"Name": self.record_type_name}}
        self.sf.updates(self.opportunities(), update)


class Account(SalesforceObject):

    api_name = "Account"

    def __init__(self, sf_connection=None):
        super().__init__(sf_connection)

        self.id = None
        self.name = None
        self.created = False
        self.website = None
        self.shipping_street = None
        self.shipping_city = None
        self.shipping_postalcode = None
        self.shipping_state = None
        self.record_type_name = "Household"

    def _format(self):
        return {
            "Website": self.website,
            "RecordType": {"Name": self.record_type_name},
            "Name": self.name,
            "ShippingStreet": self.shipping_street,
            "ShippingCity": self.shipping_city,
            "ShippingPostalCode": self.shipping_postalcode,
            "ShippingState": self.shipping_state,
        }

    def __str__(self):
        return f"{self.id}: {self.name} ({self.website})"

    @classmethod
    def get_or_create(
        cls,
        record_type_name="Household",
        website=None,
        name=None,
        shipping_city=None,
        shipping_street=None,
        shipping_state=None,
        shipping_postalcode=None,
        sf_connection=None,
    ):
        account = cls.get(
            record_type_name=record_type_name,
            website=website,
            sf_connection=sf_connection,
        )
        if account:
            return account
        account = Account()
        account.website = website
        account.name = name
        account.shipping_city = shipping_city
        account.shipping_postalcode = shipping_postalcode
        account.shipping_state = shipping_state
        account.shipping_street = shipping_street
        account.record_type_name = record_type_name
        account.save()
        return account

    @classmethod
    def get(
        cls, record_type_name="Household", website=None, name=None, sf_connection=None
    ):
        """
        Right now we're only using the website to search for existing accounts.
        """

        sf = SalesforceConnection() if sf_connection is None else sf_connection

        query = f"""
            SELECT Id, Name, Website
            FROM Account WHERE
            RecordType.Name IN ('{record_type_name}')
        """
        response = sf.query(query)

        # We do a fuzzy search on the website and if the top hit
        # has a confidence of 95 or higher we use it.
        website_idx = {
            x["Website"]: {"id": x["Id"], "name": x["Name"]}
            for x in response
            if x["Website"] is not None and x["Website"] != "NULL"
        }
        url_list = list(website_idx.keys())

        extracted = process.extractOne(website, url_list)
        logging.debug(extracted)
        if extracted is None:
            return None
        url, confidence = extracted
        if confidence < 95:
            return None
        account = Account()
        account.id = website_idx[url]["id"]
        account.name = website_idx[url]["name"]
        account.website = url
        account.created = False

        return account

    def save(self):
        self.sf.save(self)


class Contact(SalesforceObject):

    api_name = "Contact"

    def __init__(self, sf_connection=None):
        super().__init__(sf_connection)

        self.id = None
        self.account_id = None
        self.first_name = None
        self.last_name = None
        self.created = False
        self.email = None
        self.lead_source = "Stripe"
        self.mailing_postal_code = None
        self.duplicate_found = False
        self.work_email = None

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def parse_all_email(email, results):
        """
        This field is a CSV. So we parse that to make sure we've got an exact match and not just a substring match.
        """
        filtered_results = list()
        for item in results:
            all_email = item["All_In_One_EMail__c"].lower()
            buffer = StringIO(all_email)
            reader = csv.reader(buffer, skipinitialspace=True)
            if email.lower() in list(reader)[0]:
                filtered_results.append(item)
        return filtered_results

    def _format(self):
        return {
            "Email": self.email,
            "FirstName": self.first_name,
            "LastName": self.last_name,
            "LeadSource": self.lead_source,
            "MailingPostalCode": self.mailing_postal_code,
            "npe01__WorkEmail__c": self.work_email,
        }

    @classmethod
    def get_or_create(cls, email, first_name=None, last_name=None, zipcode=None):
        contact = cls.get(email=email)
        if contact:
            logging.debug(f"Contact found: {contact}")
            return contact
        logging.debug("Creating contact...")
        contact = Contact()
        contact.email = email
        contact.first_name = first_name
        contact.last_name = last_name
        contact.mailing_postal_code = zipcode
        contact.save()
        return contact

    @classmethod
    def get(cls, id=None, email=None, sf_connection=None):

        sf = SalesforceConnection() if sf_connection is None else sf_connection

        if id is None and email is None:
            raise SalesforceException("id or email must be specified")
        if id and email:
            raise SalesforceException("id and email can't both be specified")
        if id:
            query = f"""
                    SELECT Id, AccountId, FirstName, LastName, LeadSource, Stripe_Customer_ID__c, MailingPostalCode, Email, npe01__WorkEmail__c
                    FROM Contact
                    WHERE id = '{id}'
                    """
            response = sf.query(query)
            # should only be one result here because we're
            # querying by id
            response = response[0]
            contact = Contact()
            contact.id = response["Id"]
            contact.account_id = response["AccountId"]
            contact.first_name = response["FirstName"]
            contact.last_name = response["LastName"]
            contact.email = response["Email"]
            contact.lead_source = response["LeadSource"]
            contact.mailing_postal_code = response["MailingPostalCode"]
            contact.work_email = response["npe01__WorkEmail__c"]
            contact.created = False
            return contact

        query = f"""
                SELECT Id, AccountId, FirstName, LastName, LeadSource, MailingPostalCode, All_In_One_EMail__c, Email, npe01__WorkEmail__c
                FROM Contact
                WHERE All_In_One_EMail__c
                LIKE '%{email}%'
                """

        response = sf.query(query)
        if not response:
            return None
        response = cls.parse_all_email(email=email, results=response)
        if not response:
            return None
        contact = Contact()
        if len(response) > 1:
            contact.duplicate_found = True
        response = response[0]
        contact.id = response["Id"]
        contact.account_id = response["AccountId"]
        contact.first_name = response["FirstName"]
        contact.last_name = response["LastName"]
        contact.email = response["Email"]
        contact.lead_source = response["LeadSource"]
        contact.work_email = response["npe01__WorkEmail__c"]
        contact.mailing_postal_code = response["MailingPostalCode"]
        contact.created = False

        return contact

    def __str__(self):
        return f"{self.id} ({self.account_id}): {self.first_name} {self.last_name}"

    def save(self):
        self.sf.save(self)
        # TODO this is a workaround for now because creating a new
        # contact will also create a new account and we need that account ID
        # so we have to re-fetch the contact to get it
        tmp_contact = self.get(id=self.id)
        self.account_id = tmp_contact.account_id


class Affiliation(SalesforceObject):
    """
    This object is a link between a contact and an account.
    """

    api_name = "npe5__Affiliation__c"

    def __init__(self, contact=None, account=None, role=None, sf_connection=None):
        super().__init__(sf_connection)
        # TODO allow id to be set in __init__?
        self.id = None
        self.contact = contact.id
        self.account = account.id
        self.role = role

    @classmethod
    def get(cls, contact, account, sf_connection=None):

        sf = SalesforceConnection() if sf_connection is None else sf_connection

        query = f"""
            SELECT Id, npe5__Role__c from npe5__Affiliation__c
            WHERE npe5__Contact__c = '{contact.id}'
            AND npe5__Organization__c = '{account.id}'
        """
        response = sf.query(query)

        if not response:
            return None

        if len(response) > 1:
            raise SalesforceException("More than one affiliation found")
        role = response[0]["npe5__Role__c"]

        affiliation = Affiliation(contact=contact, account=account, role=role)
        affiliation.id = response[0]["Id"]
        return affiliation

    @classmethod
    def get_or_create(cls, account=None, contact=None, role=None):
        affiliation = cls.get(account=account, contact=contact)
        if affiliation:
            return affiliation
        affiliation = Affiliation(account=account, contact=contact, role=role)
        affiliation.save()
        return affiliation

    def save(self):
        self.sf.save(self)

    def __str__(self):
        return (
            f"{self.id}: {self.contact} is affiliated with {self.account} ({self.role})"
        )

    def _format(self):
        return {
            "npe5__Contact__c": self.contact,
            "npe5__Role__c": self.role,
            "npe5__Organization__c": self.account,
        }


class Task(SalesforceObject):

    api_name = "Task"

    def __init__(self, owner_id=None, what_id=None, subject=None, sf_connection=None):
        super().__init__(sf_connection)
        self.owner_id = owner_id
        self.what_id = what_id
        self.subject = subject

    def save(self):
        self.sf.save(self)

    def __str__(self):
        return f"{self.subject}"

    def _format(self):
        return {
            "OwnerId": self.owner_id,
            "WhatId": self.what_id,
            "Subject": self.subject,
        }


class User(SalesforceObject):

    api_name = "User"

    def __init__(self, sf_connection=None):
        super().__init__(sf_connection)

    def __str__(self):
        return f"{self.id}: {self.username}"

    @classmethod
    def get(cls, username, sf_connection=None):

        sf = SalesforceConnection() if sf_connection is None else sf_connection

        query = f"""
            SELECT Id, Username FROM User
            WHERE username = '{username}'
        """
        response = sf.query(query)

        if not response:
            return None

        user = User()
        user.id = response[0]["Id"]
        user.username = response[0]["Username"]
        return user
