import os

MEMBERSHIP_RECORDTYPEID = '01216000001IhHp'
DONATION_RECORDTYPEID = '01216000001IhI9'

stripe_keys = {
    'secret_key': os.environ['SECRET_KEY'],
    'publishable_key': os.environ['PUBLISHABLE_KEY']
}

FLASK_SECRET_KEY = os.environ['FLASK_SECRET_KEY']

SALESFORCE = {
    "CLIENT_ID": os.environ['SALESFORCE_CLIENT_ID'],
    "CLIENT_SECRET": os.environ['SALESFORCE_CLIENT_SECRET'],
    "USERNAME": os.environ['SALESFORCE_USERNAME'],
    "PASSWORD": os.environ['SALESFORCE_PASSWORD'],
    "HOST": os.environ["SALESFORCE_HOST"]
}
