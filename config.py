from datetime import timedelta
import os


def bool_env(val):
    """Replaces string based environment values with Python booleans"""
    return True if os.environ.get(val, False) == 'True' else False

TIMEZONE = "US/Central"
FLASK_SECRET_KEY = os.environ['FLASK_SECRET_KEY']

########
# Celery
#
CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
CELERY_RESULT_BACKEND = os.environ['CELERY_RESULT_BACKEND']
CELERY_ALWAYS_EAGER = bool_env('CELERY_ALWAYS_EAGER')
CELERYBEAT_SCHEDULE = {
        'every-minute': {
            'task': 'batch.charge_cards',
            'schedule': timedelta(seconds=10)
            },
        }

######
# SMTP
#
# TODO: pull these from env:
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
# TODO: add Texas Weekly record type
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

########
# Sentry
#
ENABLE_SENTRY = bool_env('ENABLE_SENTRY')
SENTRY_DSN = os.environ['SENTRY_DSN']
