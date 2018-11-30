import builtins
import csv
import re
import json
import logging
import os
from pprint import pprint  # TODO rm
from datetime import datetime
from decimal import Decimal
from io import StringIO

import requests
from pytz import timezone

from fuzzywuzzy import process

log = logging.getLogger(__name__)

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


class SalesforceException(Exception):
    pass


class SalesforceConnection:

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

        r = requests.post(self.url, data=self.payload)
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
    def check_response(response, expected_status=200):
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
            log.exception(f"Exception in check_response: {e}")
        if code != expected_status:
            e = SalesforceException(f"Expected {expected_status} but got {code}")
            try:
                e.content = content[0]
            except NameError:
                e.content = None
            except KeyError:
                e.content = content
            e.response = response
            log.error(f"response.text: {response.text}")
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
        log.debug(query)
        r = requests.get(url, headers=self.headers, params=payload)
        self.check_response(r)
        response = json.loads(r.text)
        # recursively get the rest of the records:
        if response["done"] is False:
            return response["records"] + self.query(
                query=None, path=response["nextRecordsUrl"]
            )
        log.debug(response)
        return response["records"]

    def post(self, path, data):
        """
        Call the Salesforce API to make inserts.
        """
        url = f"{self.instance_url}{path}"
        resp = requests.post(url, headers=self.headers, data=json.dumps(data))
        response = json.loads(resp.text)
        self.check_response(response=resp, expected_status=201)
        log.debug(response)
        return response

    def patch(self, path, data, expected_response=204):
        """
        Call the Saleforce API to make updates.
        """

        url = f"{self.instance_url}{path}"
        log.debug(data)
        resp = requests.patch(url, headers=self.headers, data=json.dumps(data))
        self.check_response(response=resp, expected_status=expected_response)
        return resp

    def describe(self, object_name):
        path = (
            f"/services/data/{SALESFORCE_API_VERSION}/sobjects/{object_name}/describe/"
        )
        return self.get(path)

    def get(self, path, fields=None):
        """
        Call the Saleforce API to retrieve an object.
        """
        url = f"{self.instance_url}{path}"
        if fields:
            url += "?{','.join(fields)}"
        log.debug(url)
        resp = requests.get(url, headers=self.headers)
        self.check_response(response=resp, expected_status=200)
        resp = json.loads(resp.text)
        return resp

    def updates(self, objects, changes):

        if not objects:
            raise SalesforceException("at least one object must be specified")

        data = dict()
        # TODO generate data below in a separate function
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
        log.debug(response)
        error = False
        for item in response:
            if item["success"] is not True:
                log.warning(f"{item['errors']}")
                error = item["errors"]
        if error:
            raise SalesforceException(f"Failure on update: {error}")

        return response

    def save(self, sf_object):

        if sf_object.id:
            if (
                not sf_object.tainted
            ):  # TODO or should we test to see if serialize() is empty?
                log.warning(f"{sf_object.api_name} has no changes to save")
                return

            log.info(f"{sf_object.api_name} object already exists; updating...")
            log.debug(sf_object.serialize())
            path = f"/services/data/{SALESFORCE_API_VERSION}/sobjects/{sf_object.api_name}/{sf_object.id}"
            try:
                response = self.patch(path=path, data=sf_object.serialize())
            except SalesforceException as e:
                log.exception(e.response.text)
                raise
            return

        log.info(f"{sf_object.api_name} object doesn't exist; creating...")
        path = f"/services/data/{SALESFORCE_API_VERSION}/sobjects/{sf_object.api_name}"
        try:
            response = self.post(path=path, data=sf_object.serialize())
        except SalesforceException as e:
            log.exception(e.response.text)
            raise

        sf_object.id = response["id"]
        sf_object.created = True
        sf_object.tainted = set()
        return


class SalesforceObject(object):
    """
    This is the parent of all the other Salesforce objects.
    """

    @property
    @classmethod
    def api_name(cls):
        raise NotImplementedError

    @staticmethod
    def make_maps(fields):
        attr_to_field_map = dict()
        for field in fields:
            attr = SalesforceObject.snake_case(field)
            if attr in attr_to_field_map.keys():
                log.warning(f"Duplicate attribute name: {attr} ({field})")
                attr = field.lower()
            attr_to_field_map[attr] = field
        field_to_attr_map = {v: k for k, v in attr_to_field_map.items()}
        return attr_to_field_map, field_to_attr_map

    @classmethod
    def get_schema(cls):
        log.warning("called schema()")
        sf = SalesforceConnection()  # TODO pass this in?
        schema = sf.describe(cls.api_name)
        cls.attr_to_field_map, cls.field_to_attr_map = cls.make_maps(
            [x["name"] for x in schema["fields"]]
        )
        # TODO do type-checking for certain fields? Like those with picklists? Or
        # numbers? Or those that are updateable=False?

    def _format(self):
        raise NotImplementedError

    def deserialize(self, response):
        cls = type(self)
        cls.attr_to_field_map, cls.field_to_attr_map = cls.make_maps(response.keys())
        for field, value in response.items():
            # not using setattr() because we don't want to set tainted in our __setattr__
            self.__dict__[cls.field_to_attr_map[field]] = value

    @classmethod
    def deserialize_group(cls, response):
        group = list()
        # TODO make this a list comprehension
        for item in response:
            obj = cls()
            obj.deserialize(item)
            group.append(obj)
        return group

    def __repr__(self):
        obj = self.serialize()
        return json.dumps(obj)

    def fetch(self, sf_connection=None):
        cls = type(self)
        log.info(f"Calling fetch() on {cls}")

        if cls.__name__ == "SalesforceObject":
            raise NotImplementedError

        sf = SalesforceConnection() if sf_connection is None else sf_connection

        # TODO restrict by fields if present?
        path = f"/services/data/{SALESFORCE_API_VERSION}/sobjects/{self.api_name}/{self.id}"
        log.debug(path)
        response = sf.get(path)
        cls = type(self)
        # TODO: isn't everything below the same as deserialize()?
        cls.attr_to_field_map, cls.field_to_attr_map = cls.make_maps(response.keys())
        for field, value in response.items():
            attr = cls.field_to_attr_map[field]
            if attr in self.__dict__ and self.__dict__[attr] != value:
                log.warning(
                    f"Overwriting value of {attr} ({self.__dict__[attr]}) on {cls} to {value}"
                )
            # not using setattr() because we don't want to set tainted in our __setattr__
            self.__dict__[cls.field_to_attr_map[field]] = value

    def __getattr__(self, attr):
        # TODO what about the case where the field map was generated from a SELECT so it
        # already exists but they request something that does actually exist but hasn't
        # been fetched yet? Call fetch() only if:
        # 1. The field map exists
        # 2. the attr isn't in it
        # 3. the schema hasn't been fetched
        #    if the value is found after the fetch then warn that maybe it should be a
        #    default field
        #    TODO create an empty field map if it doeesn't exist in __init__ so we don't
        #    have to test if it exists?
        name = f"{type(self).__name__}.{attr}"
        log.debug(f"Getting {attr} from {type(self).__name__}")
        if (
            "attr_to_field_map" in type(self).__dict__
            and attr not in self.attr_to_field_map.keys()
        ):
            log.debug(
                f"attr_to_field_map not present or {attr} not in attr_to_field_map"
            )
            raise AttributeError(f"{name} not in map")

        if "id" not in self.__dict__ or not self.__dict__["id"]:
            log.debug("id not in dict; can't fetch")
            raise AttributeError(f"No 'id' so can't fetch {name}")
        if self.tainted:
            log.warning(
                f"Overwriting value(s) of {','.join(self.tainted)} on {type(self)}"
            )
        log.debug(f"Fetching {type(self)} {self.id}")
        self.fetch()
        if attr in self.__dict__:
            return getattr(self, attr)
        raise AttributeError(f"{name}")

    def __setattr__(self, attr, value):
        log.debug(f"Setting {attr} to {value} on {type(self)}")
        # TODO: i think there's a reason I didn't the super() outside of the hasattr but
        # I can't remember what it is
        # TODO don't taint it if it's already set to the same value?
        # TODO right now if we get the attr name wrong it will set it but will silently
        # skip/fail when serializing -- a way to fix this?
        # TODO should we only add to tainted if the map exists and it's in there?
        if attr in self.__dict__:
            super().__setattr__(attr, value)
            if attr != "id" and attr != "tainted":
                logging.debug(f"Marking {self.api_name}.{attr} as tainted")
                self.tainted.add(attr)
        else:
            super().__setattr__(attr, value)

    def my_save(self):  # TODO rm
        self.sf.save(self)
        self.tainted = set()
        return self

    # TODO __getattr__ fetch on demand? If so we don't have to fetch the account_id from a new contact
    # TODO list of fields to grab on SELECT for each type of object? Does it have to be api names or can we fetch the schema?
    # TODO use composite request to create Contact/Account/Opportunity in one API call?
    # TODO use related API query to get opps for an RDO?
    def serialize(self):
        # don't differentiate patch() vs post() here and let that happen (by removing
        # what's not tainted) in the save() method? Because right now we're testing for
        # "id" in both places and that feels ugly and redundant
        log.debug("called serialize")
        # TODO construct the reverse map here and in deserialize() on demand since here and deserialize() are
        # the only places we use it?
        if not hasattr(self, "field_to_attr_map"):
            self.get_schema()
        out = dict()
        if hasattr(self, "id") and self.id is not None:  # object exists; use tainted
            for attribute in self.tainted:
                if attribute == "id":
                    # id is always in the URL not the body
                    continue
                if attribute not in self.attr_to_field_map:
                    # we don't want .created and .duplicate_found
                    continue
                out[self.attr_to_field_map[attribute]] = getattr(self, attribute)
        else:
            out = {
                api_name: getattr(self, attribute)
                for api_name, attribute in self.field_to_attr_map.items()
                if attribute in self.__dict__
            }
            del out["Id"]
        # TODO get this on the deserialize too
        if hasattr(self, "record_type_name") and self.record_type_name is not None:
            out["RecordType"] = {"Name": self.record_type_name}

        return out

    def __init__(self, sf_connection=None):
        self.tainted = set()
        self.id = None
        self.sf = SalesforceConnection() if sf_connection is None else sf_connection
        self.created = False

    @staticmethod
    def snake_case(name):
        output = name
        # remove leading chars:
        if not output.islower():
            output = re.sub(r"^[^A-Z]*", "", output)
        # remove trailing chars:
        output = re.sub(r"__c$", "", output)
        output = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", output)
        output = re.sub("([a-z0-9])([A-Z])", r"\1_\2", output).lower()
        output = re.sub(r"__+", "_", output)
        log.debug(f"{name} -> {output}")
        return output

    # TODO does this need to be a class method?
    # TODO move this to __init__?
    @classmethod
    def get(cls, id, sf_connection=None):
        log.debug(f"Calling get() on {cls}")

        if cls.__name__ == "SalesforceObject":
            raise NotImplementedError

        sf = SalesforceConnection() if sf_connection is None else sf_connection

        # TODO restrict by fields if present
        path = f"/services/data/{SALESFORCE_API_VERSION}/sobjects/{cls.api_name}/{id}"
        log.debug(path)
        response = sf.get(path)
        obj = cls()
        cls.attr_to_field_map = dict()
        cls.field_to_attr_map = dict()
        for field, value in response.items():
            attr = cls.snake_case(field)
            if attr in cls.attr_to_field_map.keys():
                log.warning(f"Duplicate attribute name: {attr} ({field})")
                # use just the lowercase api name if there's a clash.
                attr = field.lower()
            obj.__dict__[attr] = value
            cls.attr_to_field_map[attr] = field
            cls.field_to_attr_map[field] = attr
            # not using setattr() because we don't want to set tainted in our __setattr__
            # log.warning(f"Setting {attr} to {value}")

        return obj


# TODO print warning when we have to fetch a new field? So we can add that field to the defaults?


class Opportunity(SalesforceObject):

    api_name = "Opportunity"
    default_fetch_fields = [
        "id",
        "amount",
        "name",
        "stripe_customer_id",
        "description",
        "stripe_agreed_to_pay_fees",
        "account_id",
    ]

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
        self.amount = 0
        self.close_date = today
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
        # TODO parameterize stage?
        # TODO allow filter by stage name on both?
        # TODO allow filtering by anything that uses equality?

        sf = SalesforceConnection() if sf_connection is None else sf_connection
        if not hasattr(cls, "attr_to_field_map"):
            cls.get_schema()  # TODO make this automatic when attr_to_field_map is referenced?
        query_string = ",".join(
            cls.attr_to_field_map[attr] for attr in cls.default_fetch_fields
        )
        log.debug(query_string)

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
        SELECT {query_string}
        FROM Opportunity
        WHERE Expected_Giving_Date__c <= {end}
        AND Expected_Giving_Date__c >= {begin}
        AND StageName = '{stage_name}'
        """
        log.debug(query)
        response = sf.query(query)

        opportunities = cls.deserialize_group(response)

        return opportunities

    @classmethod
    def update_card(cls, opportunities, card_details, sf_connection=None):
        if not opportunities:
            raise SalesforceException("at least one Opportunity must be specified")
        sf = SalesforceConnection() if sf_connection is None else sf_connection
        print(card_details)
        return sf.updates(opportunities, card_details)

    def __str__(self):
        return f"{self.id}: {self.name} for ${self.amount:.2f} ({self.description})"

    def save(self):

        # TODO it looks like account_id isn't required; remove this?
        # TODO but stage_name and close_date are required
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
                    log.warning("bad campaign ID; retrying...")
                    self.campaign_id = None
                    self.save()
                elif e.content["fields"][0] == "Referral_ID__c":
                    log.warning("bad referral ID; retrying...")
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
        else:
            self.contact = None

        self.account_id = account.id if account is not None else None

        self.id = id
        self.type = "Recurring Donation"
        self.date_established = today
        self.amount = 0
        self.installments = None
        self.record_type_name = None
        self.stripe_card_brand = None
        self.stripe_card_expiration = None
        self.stripe_card_last_4 = None

        self.created = False

    def serialize(self):
        if self.installments:
            self.amount = str(float(self.amount) * int(self.installments))
        return super().serialize()

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
        return f"{self.id}: {self.name} for ${self.amount:.2f} ({self.description})"

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
                    log.warning("bad campaign ID; retrying...")
                    self.campaign_id = None
                    self.save()
                elif e.content["fields"][0] == "Referral_ID__c":
                    log.warning("bad referral ID; retrying...")
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
            log.warning(
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
        # TODO extract this and test it
        website_idx = {
            x["Website"]: {"id": x["Id"], "name": x["Name"]}
            for x in response
            if x["Website"] is not None and x["Website"] != "NULL"
        }
        url_list = list(website_idx.keys())

        extracted = process.extractOne(website, url_list)
        log.debug(extracted)
        if extracted is None:
            return None
        url, confidence = extracted
        if confidence < 95:
            return None
        account = Account()
        account.id = website_idx[url]["id"]
        account.name = website_idx[url]["name"]
        account.website = url

        return account

    def save(self):
        self.sf.save(self)


class Contact(SalesforceObject):

    api_name = "Contact"

    def __init__(self, id=None, sf_connection=None):
        super().__init__(sf_connection)

        self.id = id
        self.duplicate_found = False

    @staticmethod
    # TODO test
    def parse_all_email(email, results):
        """
        This field is a CSV. So we parse that to make sure we've got an exact match and not just a substring match.
        """
        filtered_results = list()
        for item in results:
            all_email = item["All_In_One_EMail__c"].lower()
            buffer = StringIO(all_email)
            reader = csv.reader(buffer)
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
        }

    @classmethod
    def get_or_create(cls, email, first_name=None, last_name=None, zipcode=None):
        contact = cls.get(email=email)
        if contact:
            log.debug(f"Contact found: {contact}")
            return contact
        log.debug("Creating contact...")
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
            contact = super().get(id=id)
            return contact
            query = f"""
                    SELECT Id, AccountId, FirstName, LastName, Email
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
            return contact

        query = f"""
                SELECT Id, AccountId, FirstName, LastName, Email
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
        contact.mailing_postal_code = response["MailingPostalCode"]

        return contact

    def __str__(self):
        return f"{self.id} ({self.account_id}): {self.first_name} {self.last_name}"

    def save(self):
        self.sf.save(self)
        # TODO this is a workaround for now because creating a new
        # contact will also create a new account and we need that account ID
        # so we have to re-fetch the contact to get it
        if not self.account_id:
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
