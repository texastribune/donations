import os

from celery.schedules import crontab

# from datetime import timedelta


def bool_env(val):
    """Replaces string based environment values with Python booleans"""
    return True if os.environ.get(val, False) == "True" else False

NEWSROOM = {
    "title": os.getenv("NEWSROOM_TITLE", "Texas Tribune"),
    "name": os.getenv("NEWSROOM_NAME", "texas"),
    'domain': os.getenv("NEWSROOM_DOMAIN", "texastribune.org"),
}
TIMEZONE = os.getenv("TIMEZONE", "US/Central")
MAX_SYNC_DAYS_DIFFERENCE = os.getenv("MAX_SYNC_DAYS_DIFFERENCE", 10)

#######
# Flask
#
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", 0)
WTF_CSRF_ENABLED = False
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

########
# Celery
#

# default is 4am and 4pm:
BATCH_HOURS = os.getenv("BATCH_HOURS", "4, 16")
CELERY_TIMEZONE = TIMEZONE
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
CELERY_ALWAYS_EAGER = bool_env("CELERY_ALWAYS_EAGER")
# deprecated:
CELERYBEAT_SCHEDULE = {
    "every-day": {
        "task": "server.batch.charge_cards",
        "schedule": crontab(minute="0", hour=BATCH_HOURS),
    }
}
REDIS_URL = os.getenv("REDIS_URL")
REDIS_BACKEND_HEALTH_CHECK_INTERVAL = 5

######
# SMTP
#
MAIL_SERVER = os.getenv("MAIL_SERVER", "localhost")
MAIL_USERNAME = os.getenv("MAIL_USERNAME", "user")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "pass")
MAIL_PORT = os.getenv("MAIL_PORT", "2525")
MAIL_USE_TLS = bool_env("MAIL_USE_TLS")
DEFAULT_MAIL_SENDER = os.getenv("DEFAULT_MAIL_SENDER", "me@myplace.org")
MULTIPLE_ACCOUNT_WARNING_MAIL_RECIPIENT = os.getenv(
    "MULTIPLE_ACCOUNT_WARNING_MAIL_RECIPIENT", ""
)
ACCOUNTING_MAIL_RECIPIENT = os.getenv("ACCOUNTING_MAIL_RECIPIENT", "")
BUSINESS_MEMBER_RECIPIENT = os.getenv("BUSINESS_MEMBER_RECIPIENT", "")

########
# Stripe
#
STRIPE_KEYS = {
    "secret_key": os.getenv("SECRET_KEY"),
    "publishable_key": os.getenv("PUBLISHABLE_KEY"),
}
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
STRIPE_PRODUCTS = {
    "membership": os.getenv("STRIPE_PRODUCT_SUSTAINING", ""),
    "bigTexMonthly": os.getenv("STRIPE_PRODUCT_BIG_TEX", ""),
    "bigTexYearly": os.getenv("STRIPE_PRODUCT_BIG_TEX", ""),
    "loneStarMonthly": os.getenv("STRIPE_PRODUCT_LONE_STAR", ""),
    "loneStarYearly": os.getenv("STRIPE_PRODUCT_LONE_STAR", ""),
    "hatsOffMonthly": os.getenv("STRIPE_PRODUCT_HATS_OFF", ""),
    "hatsOffYearly": os.getenv("STRIPE_PRODUCT_HATS_OFF", ""),
    "foundersMonthly": os.getenv("STRIPE_PRODUCT_FOUNDERS", ""),
    "foundersYearly": os.getenv("STRIPE_PRODUCT_FOUNDERS", ""),
    "ceoMonthly": os.getenv("STRIPE_PRODUCT_CEO", ""),
    "ceoYearly": os.getenv("STRIPE_PRODUCT_CEO", ""),
    "chairmanMonthly": os.getenv("STRIPE_PRODUCT_CHAIRMAN", ""),
    "chairmanYearly": os.getenv("STRIPE_PRODUCT_CHAIRMAN", ""),
    "leadershipMonthly": os.getenv("STRIPE_PRODUCT_LEADERSHIP", ""),
    "leadershipYearly": os.getenv("STRIPE_PRODUCT_LEADERSHIP", ""),
    "editorMonthly": os.getenv("STRIPE_PRODUCT_EDITOR", ""),
    "editorYearly": os.getenv("STRIPE_PRODUCT_EDITOR", ""),
    "blastMonthly": os.getenv("STRIPE_PRODUCT_BLAST", ""),
    "blastYearly": os.getenv("STRIPE_PRODUCT_BLAST", ""),
    "blastAcademicMonthly": os.getenv("STRIPE_PRODUCT_BLAST_ACADEMIC", ""),
    "blastAcademicYearly": os.getenv("STRIPE_PRODUCT_BLAST_ACADEMIC", ""),
    "blastLegislativeSession": os.getenv("STRIPE_PRODUCT_BLAST_LEGISLATIVE", ""),
    "blastSpecialSession": os.getenv("STRIPE_PRODUCT_BLAST_SPECIAL", ""),
    "blastTaxExempt": os.getenv("STRIPE_PRODUCT_BLAST_TAX_EXEMPT", ""),
    "waco": os.getenv("STRIPE_PRODUCT_WACO_SUSTAINING", ""),
}
BLAST_LEGE_CAMPAIGN_ID = os.getenv("BLAST_LEGE_CAMPAIGN_ID", "")

#######
# Slack
#
ENABLE_SLACK = bool_env("ENABLE_SLACK")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#stripe")
SLACK_CHANNEL_CANCELLATIONS = os.getenv("SLACK_CHANNEL_CANCELLATIONS", "#tech-test")
SLACK_CIRCLE_NOTIFICATIONS = os.getenv("SLACK_CIRCLE_NOTIFICATIONS", "#tech-test")
SLACK_API_KEY = os.getenv("SLACK_API_KEY")

########
# Sentry
#
ENABLE_SENTRY = bool_env("ENABLE_SENTRY")
SENTRY_DSN = os.getenv("SENTRY_DSN")
SENTRY_ENVIRONMENT = os.getenv("SENTRY_ENVIRONMENT", "unknown")
REPORT_URI = os.getenv("REPORT_URI")

########
# Recaptcha
#
RECAPTCHA_KEYS = {
    "secret_key": os.getenv("RECAPTCHA_SECRET_KEY"),
    "site_key": os.getenv("RECAPTCHA_SITE_KEY"),
}

#######
# Portal
#
ENABLE_PORTAL = bool_env("ENABLE_PORTAL")

########
# Amazon
#
MWS_ACCESS_KEY = os.getenv("MWS_ACCESS_KEY", "")
MWS_SECRET_KEY = os.getenv("MWS_SECRET_KEY", "")
AMAZON_MERCHANT_ID = os.getenv("AMAZON_MERCHANT_ID", "")
AMAZON_SANDBOX = bool_env("AMAZON_SANDBOX")
AMAZON_CAMPAIGN_ID = os.getenv("AMAZON_CAMPAIGN_ID", "")
#######
# Tasks
#
# this is User.username
CIRCLE_FAILURE_RECIPIENT = os.getenv("CIRCLE_FAILURE_RECIPIENT")

CELERYD_LOG_FORMAT = "%(levelname)s %(name)s/%(module)s:%(lineno)d - %(message)s"
CELERYD_TASK_LOG_FORMAT = "%(levelname)s %(name)s/%(module)s:%(lineno)d - %(message)s"

########
# Auth0
#
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "auth.texastribune.org")
AUTH0_PORTAL_M2M_CLIENT_ID = os.getenv("AUTH0_PORTAL_M2M_CLIENT_ID", None)
AUTH0_PORTAL_M2M_CLIENT_SECRET = os.getenv("AUTH0_PORTAL_M2M_CLIENT_SECRET", None)
AUTH0_PORTAL_AUDIENCE = os.getenv(
    "AUTH0_PORTAL_AUDIENCE", "texastribune.org/portal"
)
########
# Bad Actor
#
ENABLE_BAD_ACTOR_API = bool_env("ENABLE_BAD_ACTOR_API")
BAD_ACTOR_API_URL = os.getenv("BAD_ACTOR_API_URL", None)
BAD_ACTOR_NOTIFICATION_URL = os.getenv("BAD_ACTOR_NOTIFICATION_URL", None)
BLOCK_LIST = os.getenv("BLOCK_LIST", None)

########
# Waco
#
ENABLE_WACO = bool_env("ENABLE_WACO")
WACO_CAMPAIGN_ID = os.getenv("WACO_CAMPAIGN_ID", None)
