#import json
import os
#import requests
#
# SMTP
#
#r = requests.get("https://mailtrap.io/api/v1/inboxes.json?api_token={}".format(
#    os.environ['MAILTRAP_API_TOKEN']))
#credentials = json.loads(r.text)[0]

#MAIL_SERVER = credentials['domain']
#MAIL_USERNAME = credentials['username']
#MAIL_PASSWORD = credentials['password']
#MAIL_PORT = credentials['smtp_ports'][0]
MAIL_SERVER = 'mailtrap.io'
MAIL_USERNAME = '504457b33043741d5'
MAIL_PASSWORD = '5484376211e6b6'
MAIL_PORT = '2525'

MAIL_USE_TLS = True
DEFAULT_MAIL_SENDER = 'salesforce@texastribune.org'

#
# Salesforce
#
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
