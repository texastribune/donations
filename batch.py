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
    """
    This encapulates sending to the console/stdout and email all in one.

    """
    def __init__(self):
        self.log = list()

    def it(self, string):
        """
        Add something to the log.
        """
        print(string)
        self.log.append(string)

    def send(self):
        """
        Send the assembled log out as an email.
        """
        body = '\n'.join(self.log)
        recipient = 'dcraigmile@texastribune.org'   # TODO
        subject = 'Batch run'
        send_email(body=body, recipient=recipient, subject=subject)


def amount_to_charge(entry):
    """
    Determine the amount to charge. This depends on whether the payer agreed
    to pay fees or not. If they did then we add that to the amount charged.
    Stripe charges 2.9% + $0.30.

    Stripe wants the amount to charge in cents. So we multiply by 100 and
    return that.
    """
    amount = int(entry['Amount'])
    if entry['Stripe_Agreed_to_pay_fees__c']:
        fees = amount * .029 + .30
    else:
        fees = 0
    total = amount + fees
    total_in_cents = total * 100

    return total_in_cents


@celery.task()
def charge_cards():

    log = Log()

    print('---Starting batch job...')

    three_days_ago = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    today = datetime.now().strftime('%Y-%m-%d')

    query = """
        SELECT Amount, Name, Stripe_Customer_Id__c, Description,
            Stripe_Agreed_to_pay_fees__c
        FROM Opportunity
        WHERE CloseDate <= {}
        AND CloseDate >= {}
        AND StageName = 'Pledged'
        AND Stripe_Customer_Id__c != ''
        """.format(today, three_days_ago)

    print(query)
    sf = SalesforceConnection()

    response = sf.query(query)
    # TODO: check response code

    log.it('Found {} opportunities available to process.'.format(
        len(response)))

    for item in response:
        # print (item)
        amount = amount_to_charge(item)
        try:
            log.it("---- Charging ${} to {} ({})".format(amount,
                item['Stripe_Customer_ID__c'],
                item['Name']))
            charge = stripe.Charge.create(
                    customer=item['Stripe_Customer_ID__c'],
                    amount=amount,
                    currency='usd',
                    description=item['Description'],
                    )
        except stripe.error.CardError as e:
            log.it("The card has been declined: {}".format(e))
            raise Exception('problem')
        # print ('Charge: {}'.format(charge))
        # TODO: check for success

        # print ("Charge id: {}".format(charge.id))
        # TODO: copy transaction ID too
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
            raise Exception('problem')

    log.send()

if __name__ == '__main__':
    charge_cards()
