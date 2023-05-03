"""Reprocess (older) transactions

Usage:
  reprocess.py <date>

<date> is specified in the format of YYYY-MM-DD. E.g: 2015-12-22

"""

from .config import STRIPE_KEYS, TIMEZONE

from pytz import timezone

import stripe
from .batch import Log, process_charges
from docopt import docopt

zone = timezone(TIMEZONE)

stripe.api_key = STRIPE_KEYS["secret_key"]


def charge_cards(date):

    log = Log()

    log.it("---Starting reprocess job...")

    # regular (non Circle) pledges:
    log.it("---Processing regular charges...")

    query = """
        SELECT Amount, Name, Stripe_Customer_Id__c, Description,
            Stripe_Agreed_to_pay_fees__c
        FROM Opportunity
        WHERE CloseDate = {}
        AND StageName = 'Pledged'
        AND Stripe_Customer_Id__c != ''
        AND Type != 'Giving Circle'
        """.format(
        date
    )

    process_charges(query, log)

    #
    # Circle transactions are different from the others. The Close Dates for a
    # given Circle donation are all identical. That's so that the gift can be
    # recognized all at once on the donor wall. So we use another field to
    # determine when the card is actually charged: Expected_Giving_Date__c.
    # So we process charges separately for Circles.
    #

    log.it("---Processing Circle charges...")

    query = """
        SELECT Amount, Name, Stripe_Customer_Id__c, Description,
            Stripe_Agreed_to_pay_fees__c
        FROM Opportunity
        WHERE Expected_Giving_Date__c = {}
        AND StageName = 'Pledged'
        AND Stripe_Customer_Id__c != ''
        AND Type = 'Giving Circle'
        """.format(
        date
    )

    process_charges(query, log)
    log.send()


if __name__ == "__main__":
    arguments = docopt(__doc__, version="Reprocess 1.0")
    charge_cards(arguments["<date>"])
