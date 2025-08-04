"""
This file is the entrypoint for this Flask application. Can be executed with 'flask
run', 'python app.py' or via a WSGI server like gunicorn or uwsgi.

"""
import calendar
import json
import locale
import logging
import os
import re
from datetime import datetime
from pprint import pformat

import stripe
from amazon_pay.client import AmazonPayClient
from amazon_pay.ipn_handler import IpnHandler
from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from flask_talisman import Talisman
from nameparser import HumanName
from pytz import timezone
from validate_email import validate_email

from .app_celery import make_celery
from .bad_actor import BadActor
from .charges import ChargeException, QuarantinedException, charge
from .config import (
    AMAZON_CAMPAIGN_ID,
    AMAZON_MERCHANT_ID,
    AMAZON_SANDBOX,
    BLOCK_LIST,
    ENABLE_BAD_ACTOR_API,
    ENABLE_PORTAL,
    ENABLE_SENTRY,
    ENABLE_WACO,
    FLASK_SECRET_KEY,
    LOG_LEVEL,
    MAX_SYNC_DAYS_DIFFERENCE,
    MWS_ACCESS_KEY,
    MWS_SECRET_KEY,
    NEWSROOM,
    REPORT_URI,
    SENTRY_DSN,
    SENTRY_ENVIRONMENT,
    STRIPE_PRODUCTS,
    STRIPE_WEBHOOK_SECRET,
    TIMEZONE,
    WACO_CAMPAIGN_ID,
    BLAST_LEGE_CAMPAIGN_ID,
)
from .forms import (
    BlastForm,
    BlastFormLegacy,
    BlastPromoForm,
    BusinessMembershipForm,
    CircleForm,
    DonateForm,
    WacoForm,
)
from .npsp import RDO, Account, Affiliation, Contact, Opportunity, SalesforceConnection
from .util import (
    amount_to_charge,
    clean,
    notify_slack,
    send_email_new_business_membership,
    send_multiple_account_warning,
    send_slack_message,
    send_cancellation_notification,
    name_splitter,
)

ZONE = timezone(TIMEZONE)
USE_THERMOMETER = False

DONATION_TYPE_INFO = {
    "membership": {
        "type": "Recurring Donation",
        "description": f"{NEWSROOM['title']} Sustaining Membership",
        "recurring_type": "Open",
    },
    "business_membership": {
        "type": "Business Membership",
        "description": f"{NEWSROOM['title']} Business Membership",
        "recurring_type": "Open",
    },
    "circle": {
        "type": "Giving Circle",
        "description": f"{NEWSROOM['title']} Circle Membership",
        "recurring_type": "Fixed",
    },
    "blast": {
        "type": "The Blast",
        "description": "Blast Subscription",
        "recurring_type": "Open",
    },
    "waco": {
         "type": "Waco Membership",
         "description": "Waco Bridge Sustaining Membership",
         "open_ended_status": "Open",
     },
}

if ENABLE_SENTRY:
    import sentry_sdk
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.flask import FlaskIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=SENTRY_ENVIRONMENT,
        integrations=[FlaskIntegration(), CeleryIntegration()],
    )

locale.setlocale(locale.LC_ALL, "C")
csp = {
    "default-src": ["'self'", "*.texastribune.org"],
    "font-src": [
        "'self'",
        "data:",
        "*.cloudflare.com",
        "fonts.gstatic.com",
        "use.typekit.net",
    ],
    "style-src": [
        "'self'",
        "'unsafe-inline'",
        "*.googleapis.com",
        "tagmanager.google.com",
    ],
    "img-src": [
        "'self'",
        "data:",
        "*.texastribune.org",
        "q.stripe.com",
        "www.facebook.com",
        "stats.g.doubleclick.net",
        "www.google-analytics.com",
        "www.google.com",
        "googleads.g.doubleclick.net",
        "www.googletagmanager.com",
        "p.typekit.net",
        "www.google.se",
        "www.gstatic.com",
        "www.google.iq",
        "www.google-analytics.com",
        "www.google.md",
        "www.google.com.qa",
        "www.google.ca",
        "www.google.es",
        "www.google.am",
        "www.google.de",
        "www.google.jo",
        "www.google.com.pr",
        "www.google.com.ng",
        "www.google.com.lb",
        "www.google.be",
        "www.google.se",
        "www.google.co.uk",
        "www.google.co.in",
        "srclinkapp.biz",
        "www.google.com.mx",
        "*",
    ],
    "connect-src": [
        "*.stripe.com",
        "*.texastribune.org",
        "www.google-analytics.com",
        "www.facebook.com",
        "stats.g.doubleclick.net",
        "performance.typekit.net",
        "*",
    ],
    "frame-src": [
        "'self'",
        "*.stripe.com",
        "www.googletagmanager.com",
        "www.facebook.com",
        "bid.g.doubleclick.net",
        "bid.g.doubleclick.net",
        "fonts.gstatic.com",
        "connect.facebook.net",
        "wib.capitalone.com",
        "api.pmmapads.com",
        "*",
    ],
    "script-src": [
        "data:",
        "'unsafe-inline'",
        "'unsafe-eval'",
        "*.texastribune.org",
        "www.googleadservices.com",
        "js.stripe.com",
        "*.googleapis.com",
        "connect.facebook.net",
        "www.googletagmanager.com",
        "use.typekit.net",
        "code.jquery.com",
        "checkout.stripe.com",
        "www.google-analytics.com",
        "googleads.g.doubleclick.net",
        "watcher.risd.net",
        "*",
    ],
}

stripe.api_version = "2020-03-02"


app = Flask(__name__)
Talisman(
    app,
    content_security_policy={},
    content_security_policy_report_only=True,
    content_security_policy_report_uri=REPORT_URI,
)

log_level = logging.getLevelName(LOG_LEVEL)
app.logger.setLevel(log_level)

app.secret_key = FLASK_SECRET_KEY

app.config.from_pyfile("config.py")
app.config.update(
    CELERY_ACCEPT_CONTENT=["pickle", "json"],
    CELERY_ALWAYS_EAGER=False,
    CELERY_IMPORTS=("server", "server.npsp", "server.batch"),
)
stripe.api_key = app.config["STRIPE_KEYS"]["secret_key"]

celery = make_celery(app)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    # TODO: this function is duplicated in npsp.py; I started
    # to move it to util.py but that created a circular import
    # so I punted and copied it here for now.
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


"""
Redirects, including for URLs that used to be
part of the old donations app that lived at
support.texastribune.org.
"""


@app.route("/")
@app.route("/levels.html")
@app.route("/faq.html")
@app.route("/index.html")
@app.route("/memberform")
@app.route("/donateform")
@app.route("/donate/")
def index_html_route():
    return redirect("/donate", code=302)


@app.route("/circle.html")
@app.route("/circleform")
def circle_html_route():
    query_string = request.query_string.decode("utf-8")
    return redirect("/circle?%s" % query_string, code=302)


@app.route("/blast-vip")
@app.route("/blast-promo")
@app.route("/blastform")
def blast_html_route():
    return redirect("/blast", code=302)


"""
Read the Webpack assets manifest and then provide the
scripts, including cache-busting hache, as template context.

For Heroku to compile assets on deploy, the directory it
builds to needs to already exist. Hence /static/js/prod/.gitkeep.
We don't want to version control development builds, which is
why they're compiled to /static/js/build/ instead.
"""


def get_bundles(entry):
    root_dir = os.path.dirname(os.getcwd())
    build_dir = os.path.join("server", "static", "build")
    asset_path = "/static/build/"
    bundles = {"css": "", "js": []}
    manifest_path = os.path.join(build_dir, "assets.json")
    css_manifest_path = os.path.join(build_dir, "styles.json")
    with open(manifest_path) as manifest:
        assets = json.load(manifest)
    entrypoint = assets["entrypoints"][entry]
    for bundle in entrypoint["assets"]["js"]:
        bundles["js"].append(asset_path + bundle)
    with open(css_manifest_path) as manifest:
        css_assets = json.load(manifest)
    bundles["css"] = asset_path + css_assets[entry]
    return bundles


def apply_card_details(rdo=None, customer=None):

    """
    Takes the expiration date, card brand and expiration from a Stripe object and copies
    it to an RDO. The RDO is NOT saved and must be done after calling this function.
    That's to save an API call since other RDO details will almost certainly need to be
    saved as well.
    """

    customer = stripe.Customer.retrieve(customer["id"])
    card = customer.sources.retrieve(customer.sources.data[0].id)
    year = card.exp_year
    month = card.exp_month
    day = calendar.monthrange(year, month)[1]

    rdo.stripe_card_expiration = f"{year}-{month:02d}-{day:02d}"
    rdo.stripe_card_brand = card.brand
    rdo.stripe_card_last_4 = card.last4

    return rdo


@celery.task(name="app.add_donation")
def add_donation(form=None, customer=None, donation_type=None, bad_actor_request=None):
    """
    Add a contact and their donation into SF. This is done in the background
    because there are a lot of API calls and there's no point in making the
    payer wait for them. It sends a notification about the donation to Slack (if configured).
    """
    bad_actor_response = BadActor(bad_actor_request=bad_actor_request)
    quarantine = bad_actor_response.quarantine

    form = clean(form)
    first_name = form["first_name"]
    last_name = form["last_name"]
    period = form["installment_period"]
    email = form["stripeEmail"]
    zipcode = form["zipcode"]

    logging.info("----Getting contact....")
    contact = Contact.get_or_create(
        email=email, first_name=first_name, last_name=last_name, zipcode=zipcode
    )
    logging.info(contact)

    if contact.first_name == "Subscriber" and contact.last_name == "Subscriber":
        logging.info(f"Changing name of contact to {first_name} {last_name}")
        contact.first_name = first_name
        contact.last_name = last_name
        contact.mailing_postal_code = zipcode
        contact.save()

    if contact.first_name != first_name or contact.last_name != last_name:
        logging.info(
            f"Contact name doesn't match: {contact.first_name} {contact.last_name}"
        )

    if zipcode and not contact.created and contact.mailing_postal_code != zipcode:
        contact.mailing_postal_code = zipcode
        contact.save()

    if contact.duplicate_found:
        send_multiple_account_warning(contact)

    if period is None:
        logging.info("----Creating one time payment...")
        opportunity = add_opportunity(
            contact=contact, form=form, customer=customer, quarantine=quarantine
        )
        try:
            charge(opportunity)
            logging.info(opportunity)
            notify_slack(contact=contact, opportunity=opportunity)
        except ChargeException as e:
            e.send_slack_notification()
        except QuarantinedException:
            bad_actor_response.notify_bad_actor(
                transaction_type="Opportunity", transaction=opportunity
            )
        return True

    elif donation_type == "circle":
        logging.info("----Creating circle payment...")
        rdo = add_circle_membership(
            contact=contact, form=form, customer=customer, quarantine=False
        )
    else:
        logging.info("----Creating recurring payment...")
        rdo = add_recurring_donation(
            contact=contact, form=form, customer=customer, quarantine=quarantine
        )

    # get opportunities
    opportunities = rdo.opportunities()
    today = datetime.now(tz=ZONE).strftime("%Y-%m-%d")
    opp = [
        opportunity
        for opportunity in opportunities
        if opportunity.expected_giving_date == today
    ][0]
    try:
        charge(opp)
        logging.info(rdo)
        notify_slack(contact=contact, rdo=rdo)
    except ChargeException as e:
        e.send_slack_notification()
    except QuarantinedException:
        bad_actor_response.notify_bad_actor(transaction_type="RDO", transaction=rdo)
    return True


@celery.task(name="app.add_stripe_donation")
def add_stripe_donation(form=None, customer=None, donation_type=None, bad_actor_request=None):
    """
    Add a contact and their donation into SF. This is done in the background
    because there are a lot of API calls and there's no point in making the
    payer wait for them. It sends a notification about the donation to Slack (if configured).
    """
    quarantine = False
    if donation_type in ["membership", "waco"] and ENABLE_BAD_ACTOR_API:
        bad_actor_response = BadActor(bad_actor_request=bad_actor_request)
        quarantine = bad_actor_response.quarantine

    form = clean(form)
    period = form["installment_period"]

    if quarantine:
        contact = get_or_create_contact(form)
        form["source"] = customer["id"]
        form["amount_w_fees"] = float(amount_to_charge(form))
        bad_actor_response.notify_bad_actor(
            transaction=contact,
            transaction_data=form
        )
        return True

    if period is None:
        logging.info("----Creating one time payment...")
        payment = create_payment_intent(donation_type=donation_type, customer=customer, form=form, quarantine=quarantine)
        return True
    else:
        logging.info("----Creating recurring payment...")
        if donation_type in ["membership", "waco"]:
            subscription = create_custom_subscription(donation_type=donation_type, customer=customer, form=form, quarantine=quarantine)
        else:
            subscription = create_subscription(donation_type=donation_type, customer=customer, form=form, quarantine=quarantine)
        return True


def do_charge_or_show_errors(form_data, template, bundles, function, donation_type):
    app.logger.debug("----Creating Stripe customer...")

    email = form_data["stripeEmail"]
    installment_period = form_data["installment_period"]
    amount = form_data["amount"]
    stripe_token = form_data["stripeToken"]
    name = " ".join((form_data["first_name"], form_data["last_name"]))
    shipping_city = form_data.get("shipping_city", None)
    shipping_street = form_data.get("shipping_street", None)
    shipping_state = form_data.get("shipping_state", None)
    zipcode = form_data.get("zipcode", form_data.get("shipping_postalcode", None))
    website = form_data.get("website", None)
    business_name = form_data.get("business_name", None)

    try:
        customer = stripe.Customer.create(
            email=email,
            name=name,
            address={
                "line1": shipping_street,
                "city": shipping_city,
                "state": shipping_state,
                "postal_code": zipcode,
            },
            metadata={
                "website": website,
                "business_name": business_name,
            },
            card=stripe_token
        )
        app.logger.debug("----Stripe customer created...")
    except stripe.error.CardError as e:
        body = e.json_body
        err = body.get("error", {})
        message = err.get("message", "")
        # at this point, amount has been converted to a float
        # bring it back to a string for the rehydration of the form
        form_data["amount"] = str(form_data["amount"])
        del form_data["stripeToken"]

        return render_template(
            template,
            bundles=bundles,
            stripe=app.config["STRIPE_KEYS"]["publishable_key"],
            recaptcha=app.config["RECAPTCHA_KEYS"]["site_key"],
            message=message,
            form_data=form_data,
        )
    app.logger.info(f"Customer id: {customer.id}")
    bad_actor_request = None
    try:
        bad_actor_request = BadActor.create_bad_actor_request(
            headers=request.headers,
            captcha_token=form_data["recaptchaToken"],
            email=email,
            amount=amount,
            zipcode=zipcode,
            first_name=form_data["first_name"],
            last_name=form_data["last_name"],
            remote_addr=request.remote_addr,
            reason=form_data["reason"],
        )
        app.logger.info(bad_actor_request)
    except Exception as error:
        app.logger.warning("Unable to check for bad actor: %s", error)

    function(
        customer=customer,
        form=clean(form_data),
        donation_type=donation_type,
        bad_actor_request=bad_actor_request,
    )
    if donation_type == "blast":
        charge_template = "blast-charge.html"
        bundles = get_bundles("old")
    else:
        charge_template = f"charge_{NEWSROOM['name']}.html" if donation_type != "waco" else "charge_waco.html"
        bundles = get_bundles(NEWSROOM["name"] if NEWSROOM["name"] != "texas" else "donate")
    gtm = {
        "event_value": amount,
        "event_label": "once" if installment_period == "None" else installment_period,
    }
    return render_template(charge_template, gtm=gtm, bundles=bundles, newsroom=NEWSROOM)


def validate_form(FormType, bundles, template, function=add_donation.delay):
    app.logger.info(pformat(request.form))

    form = FormType(request.form)
    # use form.data instead of request.form from here on out
    # because it includes all filters applied by WTF Forms
    form_data = form.data
    form_errors = form.errors
    email = form_data["stripeEmail"]

    # hard check on identified bad actors
    if BLOCK_LIST:
        name = form_data["first_name"] + " " + form_data["last_name"]
        if name in BLOCK_LIST and form_data["amount"] == 1:
            app.logger.error(f"Blocked potential bad actor: {name} - {email}")
            message = "There was an issue saving your donation information."
            return render_template(
                "error.html",
                message=message,
                bundles = get_bundles(NEWSROOM["name"] if NEWSROOM["name"] != "texas" else "old"),
                newsroom=NEWSROOM,
            )

    if FormType is DonateForm:
        donation_type = "membership"
        # TODO discuss when we don't need to default to the WACO_CAMPAIGN_ID
        if NEWSROOM["name"] == "waco":
            form_data["campaign_id"] = WACO_CAMPAIGN_ID
        function = add_stripe_donation.delay
    elif FormType is CircleForm:
        donation_type = "circle"
        function = add_stripe_donation.delay
    elif FormType is BlastForm:
        donation_type = "blast"
        if form_data['installment_period'] == "one-time for 2025":
            # this is the special session-only option
            # the text comes through as 'one-time for 2025', but these are yearly subscriptions in Stripe
            # we will need to close manually at the end of the session
            form_data["campaign_id"] = BLAST_LEGE_CAMPAIGN_ID
        function = add_stripe_donation.delay
    elif FormType is BlastFormLegacy:
        donation_type = "blast"
    elif FormType is BusinessMembershipForm:
        donation_type = "business_membership"
        function = add_stripe_donation.delay
    #remove this after Waco launch
    elif FormType is WacoForm:
        donation_type = "waco"
        form_data["campaign_id"] = WACO_CAMPAIGN_ID
        function = add_stripe_donation.delay
    else:
        raise Exception("Unrecognized form type")


    if not validate_email(email):
        message = "There was an issue saving your email address."
        return render_template(
            "error.html",
            message=message,
            bundles=get_bundles(NEWSROOM["name"] if NEWSROOM["name"] != "texas" else "old"),
            newsroom=NEWSROOM,
        )
    if not form.validate():
        app.logger.error(f"Form validation errors: {form_errors}")
        message = "There was an issue saving your donation information."
        return render_template(
            "error.html",
            message=message,
            bundles=get_bundles(NEWSROOM["name"] if NEWSROOM["name"] != "texas" else "old"),
            newsroom=NEWSROOM,
        )

    return do_charge_or_show_errors(
        form_data=form_data,
        bundles=bundles,
        template=template,
        function=function,
        donation_type=donation_type,
    )


@app.route("/robots.txt")
def robots_txt():
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, "app"), "robots.txt")


if ENABLE_PORTAL:

    @app.route("/account/", defaults={"path": ""})
    @app.route("/account/<path>/")
    def account(path):
        return render_template(
            "account.html",
            bundles=get_bundles("account"),
            stripe=app.config["STRIPE_KEYS"]["publishable_key"],
            recaptcha=app.config["RECAPTCHA_KEYS"]["site_key"],
        )


@app.route("/donate", methods=["GET", "POST"])
def donate_form():
    if NEWSROOM["name"] != "texas":
        bundles = get_bundles(f"{NEWSROOM['name']}")
        template = f"{NEWSROOM['name']}-form.html"
    else:
        bundles = get_bundles("donate")
        template = "donate-form.html"

    if request.method == "POST":
        return validate_form(DonateForm, bundles=bundles, template=template)

    return render_template(
        template,
        bundles=bundles,
        stripe=app.config["STRIPE_KEYS"]["publishable_key"],
        recaptcha=app.config["RECAPTCHA_KEYS"]["site_key"],
        use_thermometer=USE_THERMOMETER,
        newsroom=NEWSROOM,
    )


@app.route("/circle", methods=["GET", "POST"])
def circle_form():
    if NEWSROOM["name"] != "texas":
        return redirect(url_for("donate_form"))

    bundles = get_bundles("circle")
    template = "circle-form.html"

    if request.method == "POST":
        return validate_form(CircleForm, bundles=bundles, template=template)

    return render_template(
        template,
        bundles=bundles,
        stripe=app.config["STRIPE_KEYS"]["publishable_key"],
        recaptcha=app.config["RECAPTCHA_KEYS"]["site_key"],
    )


@app.route("/business", methods=["GET", "POST"])
def business_form():
    if NEWSROOM["name"] != "texas":
        return redirect(url_for("donate_form"))

    bundles = get_bundles("business")
    template = "business-form.html"

    if request.method == "POST":
        return validate_form(
            BusinessMembershipForm,
            bundles=bundles,
            template=template,
        )

    return render_template(
        template,
        bundles=bundles,
        stripe=app.config["STRIPE_KEYS"]["publishable_key"],
        recaptcha=app.config["RECAPTCHA_KEYS"]["site_key"],
    )

@app.route("/blast", methods=["GET", "POST"])
def blast_form():
    if NEWSROOM["name"] != "texas":
        return redirect(url_for("donate_form"))

    bundles = get_bundles("blast")
    template = "blast-form.html"

    if request.method == "POST":
        return validate_form(BlastForm, bundles=bundles, template=template)

    return render_template(
        template,
        bundles=bundles,
        stripe=app.config["STRIPE_KEYS"]["publishable_key"],
        recaptcha=app.config["RECAPTCHA_KEYS"]["site_key"],
    )


@app.route("/waco", methods=["GET", "POST"])
def waco_form():
    if not ENABLE_WACO:
        return redirect("https://support.wacobridge.org")

    bundles = get_bundles("waco")
    template = "waco-form.html"

    if request.method == "POST":
        return validate_form(WacoForm, bundles=bundles, template=template)

    return render_template(
        template,
        bundles=bundles,
        stripe=app.config["STRIPE_KEYS"]["publishable_key"],
        recaptcha=app.config["RECAPTCHA_KEYS"]["site_key"],
        use_thermometer=USE_THERMOMETER,
    )


# @app.route("/blast-promo")
def the_blast_promo_form():
    if NEWSROOM["name"] != "texas":
        return redirect(url_for("donate_form"))

    bundles = get_bundles("old")
    form = BlastPromoForm()

    campaign_id = request.args.get("campaignId", default="")
    referral_id = request.args.get("referralId", default="")

    return render_template(
        "blast-promo.html",
        form=form,
        campaign_id=campaign_id,
        referral_id=referral_id,
        amount="250",
        installment_period="yearly",
        key=app.config["STRIPE_KEYS"]["publishable_key"],
        bundles=bundles,
    )


@app.route("/submit-blast-promo", methods=["POST"])
def submit_blast_promo():
    if NEWSROOM["name"] != "texas":
        return redirect(url_for("donate_form"))

    bundles = get_bundles("old")
    app.logger.info(pformat(request.form))
    form = BlastPromoForm(request.form)

    email_is_valid = validate_email(request.form["stripeEmail"])

    if email_is_valid:
        customer = stripe.Customer.create(
            email=request.form["stripeEmail"], card=request.form["stripeToken"]
        )
        app.logger.info(f"Customer id: {customer.id}")
    else:
        message = "There was an issue saving your email address."
        return render_template("error.html", message=message, bundles=bundles, newsroom=NEWSROOM)
    if form.validate():
        app.logger.info("----Adding Blast subscription...")
        add_blast_subscription.delay(customer=customer, form=clean(request.form))
        gtm = {"event_value": "200", "event_label": "annual discounted"}
        return render_template("blast-charge.html", bundles=bundles, gtm=gtm)
    else:
        app.logger.error("Failed to validate form")
        message = "There was an issue saving your donation information."
        return render_template("error.html", message=message, bundles=bundles, newsroom=NEWSROOM)


# @app.route("/blastform")
def the_blast_form():
    if NEWSROOM["name"] != "texas":
        return redirect(url_for("donate_form"))

    bundles = get_bundles("old")
    form = BlastFormLegacy()
    if request.args.get("amount"):
        amount = request.args.get("amount")
    else:
        amount = 349
    installment_period = request.args.get("installmentPeriod")

    campaign_id = request.args.get("campaignId", default="")
    referral_id = request.args.get("referralId", default="")

    return render_template(
        "blast-form-legacy.html",
        form=form,
        campaign_id=campaign_id,
        referral_id=referral_id,
        installment_period=installment_period,
        amount=amount,
        key=app.config["STRIPE_KEYS"]["publishable_key"],
        bundles=bundles,
    )


@app.route("/submit-blast", methods=["POST"])
def submit_blast():
    if NEWSROOM["name"] != "texas":
        return redirect(url_for("donate_form"))

    bundles = get_bundles("old")
    app.logger.info(pformat(request.form))
    form = BlastFormLegacy(request.form)

    name = " ".join((request.form["first_name"], request.form["last_name"]))
    email_is_valid = validate_email(request.form["stripeEmail"])
    amount = request.form["amount"]

    if email_is_valid:
        customer = stripe.Customer.create(
            name=name,
            email=request.form["stripeEmail"],
            card=request.form["stripeToken"],
        )
        app.logger.info(f"Customer id: {customer.id}")
    else:
        message = "There was an issue saving your email address."
        return render_template("error.html", message=message, bundles=bundles, newsroom=NEWSROOM)
    if form.validate():
        app.logger.info("----Adding Blast subscription...")
        form = clean(request.form)

        if amount == "349":
            form["level"] = "blast"
            form["installment_period"] = "yearly"
            event_label = "annual"
        elif amount == "40":
            form["level"] = "blast"
            form["installment_period"] = "monthly"
            event_label = "monthly"
        elif amount == "325":
            form["level"] = "blastTaxExempt"
            form["installment_period"] = "yearly"
            event_label = "annual tax exempt"

        add_stripe_donation.delay(donation_type="blast", customer=customer, form=form)

        gtm = {"event_value": amount, "event_label": event_label}

        return render_template("blast-charge.html", bundles=bundles, gtm=gtm)
    else:
        app.logger.error("Failed to validate form")
        message = "There was an issue saving your donation information."
        return render_template("error.html", message=message, bundles=bundles, newsroom=NEWSROOM)


@app.route("/donor-advised-funds")
def daf():
    if NEWSROOM["name"] != "texas":
        return redirect(url_for("donate_form"))

    bundles = get_bundles("donate")
    template = "daf.html"

    return render_template(
        template,
        bundles=bundles,
    )

@app.route("/error")
def error():
    bundles = get_bundles(NEWSROOM["name"] if NEWSROOM["name"] != "texas" else "old")
    message = "Something went wrong!"
    return render_template("error.html", message=message, bundles=bundles, newsroom=NEWSROOM)


@app.errorhandler(404)
def page_not_found(error):
    bundles = get_bundles(NEWSROOM["name"] if NEWSROOM["name"] != "texas" else "old")
    message = "The page you requested can't be found."
    return render_template("error.html", message=message, bundles=bundles, newsroom=NEWSROOM), 404


@app.route("/.well-known/apple-developer-merchantid-domain-association")
def merchantid():
    """
    This is here to verify our domain so Stripe can support Apple Pay.
    """
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(
        os.path.join(root_dir, "app"), "apple-developer-merchantid-domain-association"
    )


# TODO why do I have to set the name here?
@celery.task(name="app.customer_source_updated")
def customer_source_updated(event):

    card_details = dict()

    # TODO update this with Opportunity fields when npsp is merged

    # we update all of these fields if any of them have changed because
    # we don't have these fields already populated; after some time that won't be
    # important

    if any(
        [
            "last4" in event["data"]["previous_attributes"],
            "brand" in event["data"]["previous_attributes"],
            "exp_year" in event["data"]["previous_attributes"],
        ]
    ):
        year = event["data"]["object"]["exp_year"]
        month = event["data"]["object"]["exp_month"]
        day = calendar.monthrange(year, month)[1]
        expiration = f"{year}-{month:02d}-{day:02d}"
        card_details["Stripe_Card_Expiration__c"] = expiration
        card_details["Stripe_Card_Brand__c"] = event["data"]["object"]["brand"]
        card_details["Stripe_Card_Last_4__c"] = event["data"]["object"]["last4"]
    else:
        logging.info("Event not relevant; discarding.")
        return

    opps = Opportunity.list(
        stage_name="Pledged", stripe_customer_id=event["data"]["object"]["customer"]
    )

    if not opps:
        return

    response = Opportunity.update_card(opps, card_details)
    logging.info(response)
    logging.info("card details updated")


@celery.task(name="app.payout_paid")
def payout_paid(event):

    payout_id = event["data"]["object"]["id"]
    # get the date of the payout
    payout_date = event["data"]["object"]["arrival_date"]
    # payout_date = stripe.Payout.retrieve(payout_id).arrival_date
    payout_date = datetime.utcfromtimestamp(payout_date).strftime("%Y-%m-%d")

    # get all of the charges in the payout
    txn_list = []
    txns = stripe.BalanceTransaction.list(payout=payout_id, type="charge", limit=100)
    for txn in txns.auto_paging_iter():
        txn_list.append(txn)

    for chunk in chunks(txn_list, 100):

        # format those ids for query
        charge_ids = [t.source for t in chunk]
        charge_ids = ", ".join(["'{}'".format(value) for value in charge_ids])
        query = f"SELECT Id FROM Opportunity WHERE Stripe_Transaction_ID__c IN ({charge_ids})"
        logging.info(query)

        # get the Opportunity Ids that go with those charges
        sfc = SalesforceConnection()
        opps_to_update = sfc.query(query)
        opps_to_update = [o["Id"] for o in opps_to_update]

        # set the payout date on those opportunities
        response = sfc.update_payout_dates(opps_to_update, payout_date)
        logging.debug(response)


@celery.task(name="app.payment_intent_succeeded")
def payment_intent_succeeded(payment_intent_id):
    payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id, expand=["invoice.subscription"])
    invoice = payment_intent["invoice"]

    if invoice:
        app.logger.info(f"Payment intent invoice: {invoice}")
        subscription = invoice.get("subscription", {})
        rerun = invoice.get("metadata", {}).get("rerun")
        try:
            stripe.PaymentIntent.modify(
                payment_intent_id,
                description=subscription.get("description", payment_intent["description"])
            )
        except stripe.error.StripeError as e:
            app.logger.error(f"Issue modifying {payment_intent['id']} with message: {e}")

        if invoice['billing_reason'] == "subscription_create" or rerun == "subscription":
            process_subscription(
                subscription=subscription,
                invoice=invoice,
            )

        if invoice['billing_reason'] != "subscription_create" or rerun == "payment":
            update_next_opportunity(
                invoice=invoice,
                rerun=rerun,
            )
    else:
        customer = stripe.Customer.retrieve(payment_intent['customer'])
        contact = get_contact(customer)
        opportunity = log_opportunity(contact, payment_intent)
        notify_slack(contact=contact, opportunity=opportunity)


@celery.task(name="app.customer_subscription_deleted")
def customer_subscription_deleted(subscription_id):
    subscription = stripe.Subscription.retrieve(subscription_id, expand=["customer", "latest_invoice.charge"])
    donation_type = subscription.get("donation_type", subscription["plan"]["metadata"].get("type", "membership"))
    customer = subscription["customer"]
    charge = subscription["latest_invoice"]["charge"]
    method = subscription["cancellation_details"].get('comment') or 'Staff'
    reason = subscription["cancellation_details"].get('reason') or charge["outcome"]["seller_message"]

    contact = Contact.get(email=customer["email"])
    rdo = close_rdo(subscription["id"], method=method, contact=contact, reason=reason)
    # if nothing is returned from close_rdo, we want to halt the process
    # after a fix is in place, the event will need to be resent from Stripe
    if rdo is None:
        return

    # notifications for ended donations
    try:
        send_cancellation_notification(contact, rdo, donation_type, reason, method)
    except Exception as e:
        app.logger.error(f"Failed to send cancellation notification: {e}")


@celery.task(name="app.subscription_schedule_updated")
def subscription_schedule_updated(event):
    app.logger.info(f"subscription schedule updated event: {event}")

    sub_schedule = event["data"]["object"]
    try:
        rdo = RDO.get(subscription_id=sub_schedule["id"])
    except Exception:
        return # if no RDO is found with the given subscription schedule id, then there is nothing to update

    subscription_id = sub_schedule["subscription"]

    if subscription_id:
        update_details = {"Stripe_Subscription_Id__c": subscription_id}
        try:
            RDO.update([rdo], update_details)
        except Exception as e:
            app.logger.error(f"Follow up with {rdo.id}. Updating recurring donation with subscription {subscription_id} failed.")
    elif not rdo.stripe_subscription:
        app.logger.warning(
            f"Subscription scheduler ({sub_schedule['id']}) for rdo ({rdo.id}) updated without a new subscription id. Follow up with the scheduler."
        )


@celery.task(name="app.setup_intent_succeeded")
def setup_intent_succeeded(setup_intent_id):
    try:
        setup_intent = stripe.SetupIntent.retrieve(setup_intent_id, expand=["latest_attempt"])
    except Exception as e:
        app.logger.error(f"In-person recurring donation failed card retrieval with error: {e}")

    metadata = setup_intent["metadata"]
    try:
        payment = stripe.Subscription.create(
            customer = setup_intent["customer"],
            default_payment_method = setup_intent["latest_attempt"]["payment_method_details"]["card_present"]["generated_card"],
            metadata = {
                "donation_type": "membership",
                "donor_selected_amount": metadata["amount"],
                "campaign_id": metadata["campaign_id"],
                "pay_fees": metadata["pay_fees"],
            },
            items = [{
                "price_data": {
                    "unit_amount": int(float(metadata["amount"]) * 100),
                    "currency": "usd",
                    "product": STRIPE_PRODUCTS["membership"],
                    "recurring": {"interval": metadata["interval"]},
                }
            }]
        )
    except Exception as e:
        app.logger.error(f"In-person recurring donation failed subscription creation with error: {e}")


@celery.task(name="app.authorization_notification")
def authorization_notification(payload):

    amzn_id = payload["AuthorizationNotification"]["AuthorizationDetails"][
        "AmazonAuthorizationId"
    ]

    # trim everything after the last dash - seems like there should be a more
    # straightforward way to do this
    match = re.search("^(.*)[-]", amzn_id)
    amzn_id = match.group(1)
    logging.info(amzn_id)

    client = AmazonPayClient(
        mws_access_key=MWS_ACCESS_KEY,
        mws_secret_key=MWS_SECRET_KEY,
        merchant_id=AMAZON_MERCHANT_ID,
        region="na",
        currency_code="USD",
        sandbox=AMAZON_SANDBOX,
    )
    response = client.get_order_reference_details(amazon_order_reference_id=amzn_id)
    response = response.to_dict()

    logging.info(json.dumps(response, indent=4))

    details = response["GetOrderReferenceDetailsResponse"][
        "GetOrderReferenceDetailsResult"
    ]["OrderReferenceDetails"]

    amount = details["OrderTotal"]["Amount"]
    logging.info(amount)
    name = HumanName(details["Buyer"]["Name"])
    first_name = name.first
    last_name = name.last
    email = details["Buyer"]["Email"]
    zipcode = get_zip(details=details)
    description = details["SellerOrderAttributes"]["StoreName"]

    logging.info("----Getting contact....")
    contact = Contact.get_or_create(
        email=email, first_name=first_name, last_name=last_name, zipcode=zipcode
    )
    logging.info(contact)

    if contact.first_name == "Subscriber" and contact.last_name == "Subscriber":
        logging.info(f"Changing name of contact to {first_name} {last_name}")
        contact.first_name = first_name
        contact.last_name = last_name
        contact.save()

    if contact.first_name != first_name or contact.last_name != last_name:
        logging.info(
            f"Contact name doesn't match: {contact.first_name} {contact.last_name}"
        )

    if zipcode and not contact.created and contact.mailing_postal_code != zipcode:
        contact.mailing_postal_code = zipcode
        contact.save()

    logging.info("----Adding opportunity...")

    opportunity = Opportunity(contact=contact, stage_name="Closed Won")
    opportunity.amount = amount
    opportunity.description = description
    opportunity.lead_source = "Amazon Alexa"
    opportunity.amazon_order_id = amzn_id
    opportunity.campaign_id = AMAZON_CAMPAIGN_ID
    opportunity.name = (
        f"[Alexa] {contact.first_name} {contact.last_name} ({contact.email})"
    )
    opportunity.save()
    logging.info(opportunity)
    notify_slack(contact=contact, opportunity=opportunity)
    if contact.duplicate_found:
        send_multiple_account_warning(contact)


def get_zip(details=None):

    try:
        return details["Destination"]["PhysicalDestination"]["PostalCode"]
    except KeyError:
        logging.info("No destination found")
    try:
        return details["BillingAddress"]["PhysicalAddress"]["PostalCode"]
    except KeyError:
        logging.info("No billing address found")
    return ""


@app.route("/amazonhook", methods=["POST"])
def amazonhook():

    payload = IpnHandler(request.data, request.headers)
    if not payload.authenticate():
        return payload.error

    payload = json.loads(payload.to_json())
    app.logger.info(json.dumps(payload, indent=2))
    notification_type = list(payload.keys())[0]

    # TODO maybe check ["AuthorizationStatus"]["State"] and only process if it's "Closed"?

    if notification_type == "AuthorizationNotification":
        authorization_notification.delay(payload)
    else:
        app.logger.info("ignoring event")

    return "", 200


@app.route("/stripehook", methods=["POST"])
def stripehook():
    payload = request.data.decode("utf-8")
    signature = request.headers.get("Stripe-Signature", None)

    try:
        event = stripe.Webhook.construct_event(
            payload, signature, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        app.logger.warning("Error while decoding event!")
        return "Bad payload", 400
    except stripe.error.SignatureVerificationError:
        app.logger.warning("Invalid signature!")
        return "Bad signature", 400

    app.logger.info(f"Received event: id={event.id}, type={event.type}")

    process_stripe_event(event)

    return "Success", 200


def process_stripe_event(event):
    event_type = event["type"]
    event_object = event["data"]["object"]
    # setting celery's delay on these keeps the stripe call from erroring out
    if event_type == "customer.source.updated":
        customer_source_updated.delay(event)
    if event_type == "payout.paid":
        payout_paid.delay(event)
    if event_type == "customer.subscription.created":
        # this is now routed through the payment_intent.succeeded listener
        # which handles this bit of business in the process_subscription func
        pass
    if event_type == "payment_intent.succeeded":
        payment_intent_succeeded.delay(event_object["id"])
    if event_type == "customer.subscription.deleted":
        app.logger.info(f"subscription deleted event: {event}")
        customer_subscription_deleted.delay(event_object["id"])
    if event_type == "subscription_schedule.updated":
        subscription_schedule_updated.delay(event)
    if event_type == "setup_intent.succeeded":
        app.logger.info(f"setup intent succeeded event: {event}")
        setup_intent_succeeded.delay(event_object["id"])

    return True


def sync_stripe_event(event):
    stripe_event = stripe.Event.retrieve(event)

    process_stripe_event(stripe_event)

    return stripe_event


# this is just a temp func version of a piece of add_donation we're
# reusing for quarantined records during the move to stripe subscriptions
def get_or_create_contact(form=None):
    first_name = form["first_name"]
    last_name = form["last_name"]
    email = form["stripeEmail"]
    zipcode = form["zipcode"]

    logging.info("----Getting contact....")
    contact = Contact.get_or_create(
        email=email, first_name=first_name, last_name=last_name, zipcode=zipcode
    )
    logging.info(contact)

    if contact.first_name == "Subscriber" and contact.last_name == "Subscriber":
        logging.info(f"Changing name of contact to {first_name} {last_name}")
        contact.first_name = first_name
        contact.last_name = last_name
        contact.mailing_postal_code = zipcode
        contact.save()

    if contact.first_name != first_name or contact.last_name != last_name:
        logging.info(
            f"Contact name doesn't match: {contact.first_name} {contact.last_name}"
        )

    if zipcode and not contact.created and contact.mailing_postal_code != zipcode:
        contact.mailing_postal_code = zipcode
        contact.save()

    if contact.duplicate_found:
        send_multiple_account_warning(contact)

    return contact


def add_opportunity(contact=None, form=None, customer=None, quarantine=False):
    """
    This will add a single donation to Salesforce.
    """

    logging.info("----Adding opportunity...")

    opportunity = Opportunity(contact=contact)
    opportunity.amount = form.get("amount", 0)
    opportunity.stripe_customer = customer["id"]
    opportunity.campaign_id = form["campaign_id"]
    opportunity.referral_id = form["referral_id"]
    opportunity.description = "Texas Tribune Membership"
    opportunity.agreed_to_pay_fees = form["pay_fees_value"]
    opportunity.encouraged_by = form["reason"]
    opportunity.lead_source = "Stripe"
    opportunity.quarantined = quarantine

    customer = stripe.Customer.retrieve(customer["id"])
    card = customer.sources.retrieve(customer.sources.data[0].id)
    year = card.exp_year
    month = card.exp_month
    day = calendar.monthrange(year, month)[1]

    opportunity.stripe_card_expiration = f"{year}-{month:02d}-{day:02d}"
    opportunity.stripe_card_brand = card.brand
    opportunity.stripe_card_last_4 = card.last4

    opportunity.save()
    return opportunity


def add_circle_membership(contact=None, form=None, customer=None, quarantine=False):

    """
    This will add Circle membership to Salesforce.
    """

    if form["installment_period"] is None:
        raise Exception("installment_period must have a value")

    rdo = RDO(contact=contact)

    rdo.type = "Giving Circle"
    rdo.stripe_customer = customer["id"]
    rdo.campaign_id = form["campaign_id"]
    rdo.referral_id = form["referral_id"]
    rdo.description = "Texas Tribune Circle Membership"
    rdo.agreed_to_pay_fees = form["pay_fees_value"]
    rdo.encouraged_by = form["reason"]
    rdo.lead_source = "Stripe"
    rdo.amount = form.get("amount", 0)
    installment_period = form["installment_period"]
    if installment_period == "monthly":
        rdo.installments = 36
    else:
        rdo.installments = 3

    rdo.installment_period = installment_period
    rdo.recurring_type = "Fixed"
    rdo.quarantined = quarantine

    apply_card_details(rdo=rdo, customer=customer)
    rdo.save()

    return rdo


def add_recurring_donation(contact=None, form=None, customer=None, quarantine=False):
    """
    This will add a recurring donation to Salesforce.
    """

    if form["installment_period"] is None:
        raise Exception("installment_period must have a value")

    rdo = RDO(contact=contact)

    rdo.stripe_customer = customer["id"]
    rdo.campaign_id = form["campaign_id"]
    rdo.referral_id = form["referral_id"]
    rdo.description = "Texas Tribune Sustaining Membership"
    rdo.agreed_to_pay_fees = form["pay_fees_value"]
    rdo.encouraged_by = form["reason"]
    rdo.lead_source = "Stripe"
    rdo.amount = form.get("amount", 0)
    rdo.installments = None
    rdo.installment_period = form["installment_period"]
    rdo.recurring_type = "Open"
    rdo.quarantined = quarantine

    apply_card_details(rdo=rdo, customer=customer)
    rdo.save()

    return rdo


@celery.task(name="app.add_blast_subcription")
def add_blast_subscription(form=None, customer=None):
    """
    Adds a Blast subscription. Blast subscriptions are always recurring. They have two
    email addresses: one for billing and one for the newsletter subscription.

    """

    form = clean(form)

    first_name = form["first_name"]
    last_name = form["last_name"]
    email = form["subscriber_email"]

    logging.info("----Getting contact...")
    contact = Contact.get_or_create(
        email=email, first_name=first_name, last_name=last_name
    )
    logging.info(contact)

    rdo = RDO(contact=contact)

    rdo.stripe_customer = customer["id"]
    rdo.campaign_id = form["campaign_id"]
    rdo.referral_id = form["referral_id"]
    rdo.lead_source = "Stripe"
    rdo.amount = form.get("amount", 0)
    rdo.agreed_to_pay_fees = form["pay_fees_value"]

    # Blast specific:
    rdo.installments = 0
    rdo.description = "Blast Subscription"
    rdo.recurring_type = "Open"
    if int(float(rdo.amount)) == 40:
        rdo.installment_period = "monthly"
    else:
        rdo.installment_period = "yearly"
    now = datetime.now(tz=ZONE).strftime("%Y-%m-%d %I:%M:%S %p %Z")
    rdo.name = f"{first_name} {last_name} - {now} - The Blast"
    rdo.type = "The Blast"
    rdo.billing_email = form["stripeEmail"]
    rdo.blast_subscription_email = form["subscriber_email"]

    logging.info("----Saving RDO....")
    apply_card_details(rdo=rdo, customer=customer)
    rdo.save()
    logging.info(rdo)
    # get opportunities
    opportunities = rdo.opportunities()
    today = datetime.now(tz=ZONE).strftime("%Y-%m-%d")
    opp = [
        opportunity
        for opportunity in opportunities
        if opportunity.expected_giving_date == today
    ][0]
    try:
        charge(opp)
    except ChargeException:
        # TODO should we alert slack? Did not because we had no notifications here before.
        pass

    return True


# TODO can these funcs be moved somewhere else? (maybe util.py?)
def create_custom_subscription(donation_type=None, customer=None, form=None, quarantine=None):
    amount = amount_to_charge(form)
    source = customer["sources"]["data"][0]
    interval = "month" if form["installment_period"] == "monthly" else "year"
    donation_type_info = DONATION_TYPE_INFO[donation_type]
    subscription = stripe.Subscription.create(
        customer = customer["id"],
        default_source = source["id"],
        description = donation_type_info["description"],
        metadata = {
            "donation_type": donation_type,
            "newsroom": NEWSROOM["name"] if donation_type != "waco" else "waco",
            "donor_selected_amount": form.get("amount", 0),
            "campaign_id": form["campaign_id"],
            "referral_id": form["referral_id"],
            "pay_fees": 'X' if form["pay_fees_value"] else None,
            "encouraged_by": form["reason"],
            "quarantine": 'X' if quarantine else None,
        },
        items = [{
            "price_data": {
                "unit_amount": int(amount * 100),
                "currency": "usd",
                "product": STRIPE_PRODUCTS[donation_type],
                "recurring": {"interval": interval},
            }
        }]
    )
    return subscription


# TODO can these funcs be moved somewhere else? (maybe util.py?)
def create_subscription(donation_type=None, customer=None, form=None, quarantine=None):
    app.logger.info(f"{donation_type} form: {form}")
    period = form["installment_period"]
    product = STRIPE_PRODUCTS[form["level"]]
    prices_list = stripe.Price.list(product=product)
    price = find_price(
        prices=prices_list,
        period=period,
        pay_fees=form["pay_fees_value"],
    )

    if not price:
        app.logger.warning(f"No {form['installment_period']} price ({form['pay_fees_value']}) was found for level: {form['level']}")

    app.logger.info(f"chosen price from stripe: {price}")
    source = customer["sources"]["data"][0]
    donation_type_info = DONATION_TYPE_INFO[donation_type]
    metadata = {
        "donation_type": donation_type,
        "newsroom": NEWSROOM["name"],
        "donor_selected_amount": form.get("amount", 0),
        "campaign_id": form.get("campaign_id", None),
        "referral_id": form.get("referral_id", None),
        "pay_fees": 'X' if form["pay_fees_value"] else None,
        "encouraged_by": form.get("reason", None),
        "subscriber_email": form.get("stripeEmail", None),
        "quarantine": 'X' if quarantine else None,
    }

    if donation_type == "circle":
        subscription = stripe.SubscriptionSchedule.create(
            customer=customer["id"],
            start_date="now",
            end_behavior="cancel",
            phases=[{
                "description": donation_type_info["description"],
                "default_payment_method": source["id"],
                "items": [{
                    "price": price
                }],
                "iterations": 36 if period == "monthly" else 3,
                "metadata": metadata,
            }],
            expand=["subscription"],
        )
        # Since a subscription schedule defaults to any charge being on hold for
        # an hour before going through, we manually push through the first charge
        invoice_id = subscription.get("subscription", {}).get("latest_invoice", "")
        stripe.Invoice.finalize_invoice(invoice_id)
        stripe.Invoice.pay(invoice_id)
    else:
        subscription = stripe.Subscription.create(
            customer=customer["id"],
            default_source=source["id"],
            description=donation_type_info["description"],
            metadata=metadata,
            items=[{
                "price": price,
            }],
        )
    return subscription


def find_price(prices=[], period=None, pay_fees=False):
    nickname = "fees" if pay_fees else None
    interval = "month" if period == "monthly" else "year"

    for price in prices:
        if price["recurring"]["interval"] == interval \
            and price["nickname"] == nickname:
            return price


def create_payment_intent(donation_type=None, customer=None, form=None, quarantine=None):
    amount = amount_to_charge(form)
    payment = stripe.PaymentIntent.create(
        amount=int(amount * 100),
        currency="usd",
        customer=customer["id"],
        description=f"{NEWSROOM['title']} Membership" if donation_type != "waco" else "Waco Bridge Membership",
        metadata={
            "newsroom": NEWSROOM["name"] if donation_type != "waco" else "waco",
            "donation_type": donation_type,
            "campaign_id": form["campaign_id"],
            "referral_id": form["referral_id"],
            "pay_fees": 'X' if form["pay_fees_value"] else None,
            "encouraged_by": form["reason"],
            "quarantine": 'X' if quarantine else None,
        },
        confirm = True
    )
    return payment


def process_subscription(subscription=None, invoice=None):
    # Adds an RDO (and the pieces required therein) for different kinds of recurring donations.
    # It starts by looking for a matching Contact (or creating one).
    subscription_meta = subscription["metadata"]

    rdo_id = subscription_meta.get("rdo_id", False)
    if rdo_id:
        rdo = RDO.get(id=rdo_id)
    else:
        donation_type = subscription_meta.get("donation_type", subscription["plan"]["metadata"].get("type", "membership"))
        skip_notification = subscription_meta.get("skip_notification", False)

        if type(invoice) is str:
            invoice = stripe.Invoice.retrieve(invoice)

        invoice_status = invoice["status"]
        if invoice_status == "open":
            raise Exception(f"Subscription {subscription['id']} was created but its first invoice is still open.\
                            Please follow up with the subscription to proceed.")
        customer = stripe.Customer.retrieve(subscription["customer"])
        contact = get_contact(customer)

        # For a business membership, look for a matching Account (or create one).
        # Then add a recurring donation to the Account. Next, add an Affiliation to
        # link the Contact with the Account. Lastly, send a notification to Slack (if configured)
        # and send an email notification about the new membership.
        if donation_type == "business_membership":
            if contact.work_email is None:
                contact.work_email = contact.email
                contact.save()

            account = get_account(customer)
            rdo = log_rdo(type=donation_type, account=account, customer=customer, subscription=subscription)
            affiliation = Affiliation.get_or_create(
                account=account, contact=contact, role="Business Member Donor"
            )
            send_email_new_business_membership(account=account, contact=contact)
        else:
            rdo = log_rdo(type=donation_type, contact=contact, customer=customer, subscription=subscription)

    update_next_opportunity(
        opps=rdo.opportunities(ordered_pledges=True),
        invoice=invoice,
    )

    if not skip_notification and donation_type != "blast":
        notify_slack(contact=contact, rdo=rdo)


def get_contact(customer):
    # app.logger.info(f"Incoming customer in get_contact: {customer}")
    first_name, last_name = name_splitter(customer.get("name"))
    address = customer.get("address", None)
    zipcode = address.get("postal_code", None) if address else None
    metadata = customer.get("metadata", {})
    app.logger.info("----Getting contact....")
    contact = Contact.get_or_create(
        email=customer.get("email", None),
        first_name=first_name,
        last_name=last_name,
        zipcode=zipcode,
        id=metadata.get("sf_id", None),
    )

    # TODO had initially commented out these next two ifs but within a day the "Subscriber Subscriber"
    # issue came up, so clearly still relevant. Probably worth looking into if we can clean up the
    # data Salesforce side so we don't need to include these fix-em lines.
    if contact.first_name == "Subscriber" and contact.last_name == "Subscriber":
        app.logger.info(f"Changing name of contact to {first_name} {last_name}")
        contact.first_name = first_name
        contact.last_name = last_name
        contact.mailing_postal_code = zipcode
        contact.save()

    if contact.first_name != first_name or contact.last_name != last_name:
        app.logger.info(
            f"Contact name doesn't match: {contact.first_name} {contact.last_name}"
        )

    if zipcode and not contact.created and contact.mailing_postal_code != zipcode:
        contact.mailing_postal_code = zipcode
        contact.save()

    if contact.duplicate_found:
        send_multiple_account_warning(contact)

    return contact


def get_account(customer):
    address = customer["address"]
    metadata = customer["metadata"]

    account = Account.get_or_create(
        record_type_name="Organization",
        website=metadata.get("website", None),
        name=metadata.get("business_name", None),
        shipping_street=address.get("line1", None),
        shipping_city=address.get("city", None),
        shipping_state=address.get("state", None),
        shipping_postalcode=address.get("postal_code", None)
    )

    return account


def log_rdo(type=None, contact=None, account=None, customer=None, subscription=None):
    card = {}
    sub_meta = subscription["metadata"]
    sub_plan = subscription["plan"]
    customer_id = subscription["customer"]
    start_date = subscription["start_date"]
    donation_type_info = DONATION_TYPE_INFO[type]
    installment_period = "yearly" if sub_plan["interval"] == "year" else "monthly"
    amount = sub_meta.get("donor_selected_amount", sub_plan["metadata"].get("donor_amount", 0))

    if type == "business_membership" and account:
        rdo = RDO(account=account, date=start_date)
        year = datetime.now(tz=ZONE).strftime("%Y")
        rdo.name = f"{year} Business {account.name} Recurring"
        rdo.record_type_name = "Business Membership"
    else:
        rdo = RDO(contact=contact, date=start_date)

    if type == "blast":
        now = datetime.now(tz=ZONE).strftime("%Y-%m-%d %I:%M:%S %p %Z")
        rdo.name = f"{contact.first_name} {contact.last_name} - {now} - The Blast"
        rdo.billing_email = contact.email
        rdo.blast_subscription_email = sub_meta.get("subscriber_email", None)

    if type == "circle":
        rdo.installments = 36 if sub_plan["interval"] == "month" else 3

    rdo.amount = amount
    rdo.type = donation_type_info.get("type", None)
    rdo.newsroom = sub_meta.get("newsroom", "").lower()
    rdo.stripe_customer = customer_id
    rdo.stripe_subscription = subscription["id"]
    rdo.description = donation_type_info.get("description", None)
    rdo.campaign_id = sub_meta.get("campaign_id", None)
    rdo.referral_id = sub_meta.get("referral_id", None)
    rdo.agreed_to_pay_fees = True if sub_meta.get("pay_fees", None) else False
    rdo.encouraged_by = sub_meta.get("encouraged_by", None)
    rdo.lead_source = "Stripe"
    rdo.installment_period = installment_period
    rdo.recurring_type = donation_type_info.get("recurring_type", None)
    rdo.quarantined = True if sub_meta.get("quarantine", None) else False

    #these nested gets hit three separate fields in order to try and get a card to lookup
    source = subscription.get(
        "default_source", subscription.get(
            "default_payment_method", customer["invoice_settings"]["default_payment_method"] if customer else None))

    # attempt retrieving a card as a source and if that errors try as a payment_method
    try:
        card = stripe.Customer.retrieve_source(customer_id, source)
    except:
        try:
            payment_method = stripe.PaymentMethod.retrieve(source)
            card = payment_method["card"]
        except:
            app.logger.error(f'Stripe was not able to provide the full card information for subscription {subscription["id"]}.')

    year = card.get("exp_year", None)
    month = card.get("exp_month", None)
    if year and month:
        day = calendar.monthrange(year, month)[1]
        rdo.stripe_card_expiration = f"{year}-{month:02d}-{day:02d}"

    rdo.stripe_card_brand = card.get("brand", None)
    rdo.stripe_card_last_4 = card.get("last4", None)

    rdo.save()

    return rdo


def update_next_opportunity(opps=[], invoice=None, rerun=False):
    if not opps:
        opps = Opportunity.list(
            stage_name="Pledged",
            stripe_subscription_id=invoice["subscription"]["id"],
            asc_order=True
        )

    next_opp = opps[0]
    next_opp_date = datetime.strptime(next_opp.expected_giving_date, "%Y-%m-%d")
    charged_on_date = datetime.fromtimestamp(invoice["effective_at"])
    days_difference = abs((charged_on_date - next_opp_date).days)
    if days_difference > int(MAX_SYNC_DAYS_DIFFERENCE) and not rerun:
        raise Exception(f"""There is a large discrepancy between the charge date of invoice: {invoice["id"]}
                        and the giving date of opp: {next_opp.id} that should be reviewed before further updates.""")

    transaction_id = invoice["charge"]
    amount = invoice.get("amount_paid", 0) / 100
    charge_details = {
        "StageName": "Closed Won",
        "Stripe_Transaction_ID__c": transaction_id,
    }
    if amount:
        charge_details["Amount"] = amount

    response = Opportunity.update_stage([next_opp], charge_details)


def log_opportunity(contact, payment_intent):
    """
    This will log a single donation to Salesforce reflected from Stripe info
    """

    payment_meta = payment_intent["metadata"]
    customer_id = payment_intent["customer"]

    app.logger.info("----Adding opportunity...")

    opportunity = Opportunity(contact=contact)
    opportunity.stage_name = "Closed Won"
    opportunity.newsroom = payment_meta.get("newsroom", "").lower()
    opportunity.amount = payment_intent.get("amount", 0) / 100
    opportunity.stripe_customer = customer_id
    opportunity.stripe_transaction_id = payment_intent["latest_charge"]
    opportunity.campaign_id = payment_meta.get("campaign_id", None)
    opportunity.referral_id = payment_meta.get("referral_id", None)
    opportunity.description = payment_intent["description"]
    opportunity.agreed_to_pay_fees = True if payment_meta.get("pay_fees_value", None) else False
    opportunity.encouraged_by = payment_meta.get("encouraged_by", None)
    opportunity.lead_source = "Stripe"
    opportunity.quarantined = True if payment_meta.get("quarantined", None) else False

    card = stripe.Customer.retrieve_source(customer_id, payment_intent["source"])
    year = card.get("exp_year", None)
    month = card.get("exp_month", None)
    if year and month:
        day = calendar.monthrange(year, month)[1]
        opportunity.stripe_card_expiration = f"{year}-{month:02d}-{day:02d}"

    opportunity.stripe_card = card.get("id", None)
    opportunity.stripe_card_brand = card.get("brand", None)
    opportunity.stripe_card_last_4 = card.get("last4", None)

    opportunity.save()

    if not opportunity.stripe_card_expiration or not opportunity.stripe_card_last_4:
        app.logger.error(f'Stripe was not able to provide the full card information for opportunity {opportunity.id}.')

    return opportunity


def close_rdo(subscription_id, method=None, contact=None, reason=None):
    try:
        rdo = RDO.get(subscription_id=subscription_id)
    except Exception:
        app.logger.error(f"The recurring donation for subscription {subscription_id} was not found and the Salesforce cancellation process was halted.")
        return None

    try:
        next_opp = rdo.opportunities(ordered_pledges=True)[0]
    except Exception:
        app.logger.error(f"The next pledged opportunity for recurring donation {rdo.id} was not found and the Salesforce cancellation process was halted.")
        return None

    #first we'll mark the next opportunity "Closed Lost" and provide a reason
    opp_update_details = {
        'npsp__Closed_Lost_Reason__c': reason,
        'StageName': "Closed Lost",
    }
    Opportunity.update([next_opp], opp_update_details)

    #next we'll update the rdo to reflect the cancellation
    today = datetime.now(tz=ZONE).strftime("%Y-%m-%d")
    rdo_update_details = {
        "npsp__Status__c": "Closed",
        "Cancellation_Date__c": today,
        "Cancellation_Method__c": method,
    }
    if method == "Member Portal":
        contact_update_details = {"Requested_Recurring_Cancellation__c": today}
        Contact.update([contact], contact_update_details)

    response = RDO.update([rdo], rdo_update_details)
    app.logger.info(response)
    return rdo
