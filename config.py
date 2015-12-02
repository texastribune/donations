from datetime import timedelta
import os

TIMEZONE = "US/Central"
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

########
# Celery
#
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
CELERY_ALWAYS_EAGER = os.getenv('CELERY_ALWAYS_EAGER')  # TODO: handle boolean
CELERYBEAT_SCHEDULE = {
        'every-minute': {
            'task': 'batch.charge_cards',
            'schedule': timedelta(seconds=10)
            },
        }

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
    "CLIENT_ID": os.getenv('SALESFORCE_CLIENT_ID'),
    "CLIENT_SECRET": os.getenv('SALESFORCE_CLIENT_SECRET'),
    "USERNAME": os.getenv('SALESFORCE_USERNAME'),
    "PASSWORD": os.getenv('SALESFORCE_PASSWORD'),
    "HOST": os.getenv("SALESFORCE_HOST")
}

########
# Stripe
#
STRIPE_KEYS = {
    'secret_key': os.getenv('SECRET_KEY'),
    'publishable_key': os.getenv('PUBLISHABLE_KEY')
}
