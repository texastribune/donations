import os

########
# Celery
#
CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
CELERY_RESULT_BACKEND = os.environ['CELERY_RESULT_BACKEND']
CELERY_ALWAYS_EAGER = os.environ['CELERY_ALWAYS_EAGER']
######
# SMTP
#
MAIL_SERVER = 'mailtrap.io'
MAIL_USERNAME = '504457b33043741d5'
MAIL_PASSWORD = '5484376211e6b6'
MAIL_PORT = '2525'
MAIL_USE_TLS = True
DEFAULT_MAIL_SENDER = 'salesforce@texastribune.org'
############
# Salesforce
#
MEMBERSHIP_RECORDTYPEID = '01216000001IhHp'
DONATION_RECORDTYPEID = '01216000001IhI9'
SALESFORCE = {
    "CLIENT_ID": os.environ['SALESFORCE_CLIENT_ID'],
    "CLIENT_SECRET": os.environ['SALESFORCE_CLIENT_SECRET'],
    "USERNAME": os.environ['SALESFORCE_USERNAME'],
    "PASSWORD": os.environ['SALESFORCE_PASSWORD'],
    "HOST": os.environ["SALESFORCE_HOST"]
}
########
# Stripe
#
STRIPE_KEYS = {
    'secret_key': os.environ['SECRET_KEY'],
    'publishable_key': os.environ['PUBLISHABLE_KEY']
}
