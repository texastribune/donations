from salesforce import SalesforceConnection
import stripe
from config import STRIPE_KEYS
import requests
import json
from datetime import datetime, timedelta
import celery
from emails import send_email

stripe.api_key = STRIPE_KEYS['secret_key']


class Log(object):
    def __init__(self):
        self.log = list()

    def it(self, string):
        print(string)
        self.log.append(string)

    def send(self):
        body = '\n'.join(self.log)
        recipient = 'dcraigmile@texastribune.org'  # TODO
        subject = 'Batch run'
        send_email(body=body, recipient=recipient, subject=subject)


def process_charges(query, log):

    print(query)
    sf = SalesforceConnection()

    response = sf.query(query)
    # TODO: check response code

    log.it('Found {} opportunities available to process.'.format(
        len(response)))

    for item in response:
        # print (item)
        try:
            log.it("---- Charging ${} to {} ({})".format(item['Amount'],
                item['Stripe_Customer_ID__c'],
                item['Name']))
            charge = stripe.Charge.create(
                    customer=item['Stripe_Customer_ID__c'],
                    amount=int(item['Amount']) * 100,
                    currency='usd',
                    description=item['Description'],
                    )
        except stripe.error.CardError as e:
            log.it("The card has been declined: {}".format(e))
            continue
        except stripe.error.InvalidRequestError as e:
            log.it("Problem: {}".format(e))
            continue
        # print ('Charge: {}'.format(charge))
        # TODO: check for success

        # print ("Charge id: {}".format(charge.id))
        update = {
                'Stripe_Transaction_Id__c': charge.id,
                'Stripe_Card__c': charge.source.id,
                'StageName': 'Closed Won',
                }
        path = item['attributes']['url']
        url = '{}{}'.format(sf.instance_url, path)
        # print (url)
        resp = requests.patch(url, headers=sf.headers, data=json.dumps(update))
        # TODO: check 'errors' and 'success' too
        # print (resp)
        if resp.status_code == 204:
            log.it("ok")
        else:
            log.it("problem")
            raise Exception('problem')


@celery.task()
def charge_cards():

    log = Log()

    log.it('---Starting batch job...')

    three_days_ago = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    today = datetime.now().strftime('%Y-%m-%d')

    # regular (non Circle) pledges:
    log.it('---Processing regular charges...')

    query = """
        SELECT Amount, Name, Stripe_Customer_Id__c, Description
        FROM Opportunity
        WHERE CloseDate <= {}
        AND CloseDate >= {}
        AND StageName = 'Pledged'
        AND Stripe_Customer_Id__c != ''
        AND Type != 'Giving Circle'
        """.format(today, three_days_ago)

    process_charges(query, log)

    #
    # Circle transactions are different from the others. The Close Dates for a
    # given Circle donation are all identical. That's so that the gift can be
    # recognized all at once on the donor wall. So we use another field to
    # determine when the card is actually charged:
    # Giving_Circle_Expected_Giving_Date__c. So we process charges separately
    # for Circles.
    #

    log.it('---Processing Circle charges...')

    query = """
        SELECT Amount, Name, Stripe_Customer_Id__c, Description
        FROM Opportunity
        WHERE Giving_Circle_Expected_Giving_Date__c <= {}
        AND Giving_Circle_Expected_Giving_Date__c >= {}
        AND StageName = 'Pledged'
        AND Stripe_Customer_Id__c != ''
        AND Type = 'Giving Circle'
        """.format(today, three_days_ago)

    process_charges(query, log)
    log.send()

if __name__ == '__main__':
    charge_cards()
