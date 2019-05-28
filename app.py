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
from config import (
    FLASK_SECRET_KEY,
    LOG_LEVEL,
    TIMEZONE,
    STRIPE_WEBHOOK_SECRET,
    SENTRY_DSN,
    SENTRY_ENVIRONMENT,
    ENABLE_SENTRY,
    REPORT_URI,
    MWS_ACCESS_KEY,
    MWS_SECRET_KEY,
    AMAZON_MERCHANT_ID,
    AMAZON_SANDBOX,
    AMAZON_CAMPAIGN_ID,
)
from datetime import datetime
from pprint import pformat

from pytz import timezone

import celery
import stripe
from app_celery import make_celery
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask, redirect, render_template, request, send_from_directory
from forms import (
    BlastForm,
    BlastPromoForm,
    DonateForm,
    BusinessMembershipForm,
    CircleForm,
)
from npsp import RDO, Contact, Opportunity, Affiliation, Account
from amazon_pay.ipn_handler import IpnHandler
from amazon_pay.client import AmazonPayClient
from nameparser import HumanName
from util import (
    clean,
    notify_slack,
    send_email_new_business_membership,
    send_multiple_account_warning,
)
from validate_email import validate_email
from charges import charge

ZONE = timezone(TIMEZONE)

if ENABLE_SENTRY:
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration

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


app = Flask(__name__)
Talisman(
    app,
    content_security_policy={},
    content_security_policy_report_only=True,
    content_security_policy_report_uri=REPORT_URI,
)

limiter = Limiter(
    app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"]
)

log_level = logging.getLevelName(LOG_LEVEL)
app.logger.setLevel(log_level)
for handler in app.logger.handlers:
    limiter.logger.addHandler(handler)

app.secret_key = FLASK_SECRET_KEY

app.config.from_pyfile("config.py")
app.config.update(
    CELERY_ACCEPT_CONTENT=["pickle", "json"],
    CELERY_ALWAYS_EAGER=False,
    CELERY_IMPORTS=("app", "npsp", "batch"),
)
stripe.api_key = app.config["STRIPE_KEYS"]["secret_key"]

make_celery(app)


"""
Redirects, including for URLs that used to be
part of the old donations app that lived at
support.texastribune.org.
"""


@app.route("/blast-vip")
# @app.route("/blast-promo")
def the_blastvip_form():
    return redirect("/blastform", code=302)


@app.route("/")
@app.route("/levels.html")
@app.route("/faq.html")
@app.route("/index.html")
@app.route("/memberform")
@app.route("/donateform")
def index_html_route():
    return redirect("/donate", code=302)


@app.route("/circle.html")
@app.route("/circleform")
def circle_html_route():
    query_string = request.query_string.decode("utf-8")
    return redirect("/circle?%s" % query_string, code=302)


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
    build_dir = os.path.join("static", "build")
    asset_path = "/static/build/"
    bundles = {"css": "", "js": []}
    manifest_path = os.path.join(build_dir, "assets.json")
    css_manifest_path = os.path.join(build_dir, "styles.json")
    with open(manifest_path) as manifest:
        assets = json.load(manifest)
    entrypoint = assets["entrypoints"][entry]
    for bundle in entrypoint["js"]:
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
def add_donation(form=None, customer=None, donation_type=None):
    """
    Add a contact and their donation into SF. This is done in the background
    because there are a lot of API calls and there's no point in making the
    payer wait for them. It sends a notification about the donation to Slack (if configured).
    """

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
        opportunity = add_opportunity(contact=contact, form=form, customer=customer)
        charge(opportunity)
        logging.info(opportunity)
        notify_slack(contact=contact, opportunity=opportunity)
        return True

    elif donation_type == "circle":
        logging.info("----Creating circle payment...")
        rdo = add_circle_membership(contact=contact, form=form, customer=customer)
    else:
        logging.info("----Creating recurring payment...")
        rdo = add_recurring_donation(contact=contact, form=form, customer=customer)

    # get opportunities
    opportunities = rdo.opportunities()
    today = datetime.now(tz=ZONE).strftime("%Y-%m-%d")
    opp = [
        opportunity
        for opportunity in opportunities
        if opportunity.expected_giving_date == today
    ][0]
    charge(opp)
    logging.info(rdo)
    notify_slack(contact=contact, rdo=rdo)
    return True


def do_charge_or_show_errors(template, bundles, function, donation_type):
    app.logger.debug("----Creating Stripe customer...")

    email = request.form["stripeEmail"]
    installment_period = request.form["installment_period"]
    amount = request.form["amount"]

    try:
        customer = stripe.Customer.create(email=email, card=request.form["stripeToken"])
    except stripe.error.CardError as e:
        body = e.json_body
        err = body.get("error", {})
        message = err.get("message", "")
        form_data = request.form.to_dict()
        del form_data["stripeToken"]

        return render_template(
            template,
            bundles=bundles,
            key=app.config["STRIPE_KEYS"]["publishable_key"],
            message=message,
            form_data=form_data,
        )
    app.logger.info(f"Customer id: {customer.id}")
    function(customer=customer, form=clean(request.form), donation_type=donation_type)
    gtm = {
        "event_value": amount,
        "event_label": "once" if installment_period == "None" else installment_period,
    }
    return render_template("charge.html", gtm=gtm, bundles=get_bundles("charge"))


def validate_form(FormType, bundles, template, function=add_donation.delay):
    app.logger.info(pformat(request.form))

    form = FormType(request.form)
    if FormType is DonateForm:
        donation_type = "membership"
    elif FormType is CircleForm:
        donation_type = "circle"
    elif FormType is BlastForm:
        donation_type = "blast"
    elif FormType is BusinessMembershipForm:
        donation_type = "business_membership"
    else:
        raise Exception("Unrecognized form type")

    email = request.form["stripeEmail"]

    if not validate_email(email):
        message = "There was an issue saving your email address."
        return render_template(
            "error.html", message=message, bundles=get_bundles("old")
        )
    if not form.validate():
        app.logger.error(f"Form validation errors: {form.errors}")
        message = "There was an issue saving your donation information."
        return render_template(
            "error.html", message=message, bundles=get_bundles("old")
        )

    return do_charge_or_show_errors(
        bundles=bundles,
        template=template,
        function=function,
        donation_type=donation_type,
    )


@app.route("/donate", methods=["GET", "POST"])
def donate_form():
    bundles = get_bundles("donate")
    template = "donate-form.html"

    if request.method == "POST":
        return validate_form(DonateForm, bundles=bundles, template=template)

    return render_template(
        template, bundles=bundles, key=app.config["STRIPE_KEYS"]["publishable_key"]
    )


@app.route("/circle", methods=["GET", "POST"])
def circle_form():
    bundles = get_bundles("circle")
    template = "circle-form.html"

    if request.method == "POST":
        return validate_form(CircleForm, bundles=bundles, template=template)

    return render_template(
        template, bundles=bundles, key=app.config["STRIPE_KEYS"]["publishable_key"]
    )


@app.route("/business", methods=["GET", "POST"])
def business_form():
    bundles = get_bundles("business")
    template = "business-form.html"

    if request.method == "POST":
        return validate_form(
            BusinessMembershipForm,
            bundles=bundles,
            template=template,
            function=add_business_membership.delay,
        )

    return render_template(
        template, bundles=bundles, key=app.config["STRIPE_KEYS"]["publishable_key"]
    )


@app.route("/blast-promo")
def the_blast_promo_form():
    bundles = get_bundles("old")
    form = BlastPromoForm()

    campaign_id = request.args.get("campaignId", default="")
    referral_id = request.args.get("referralId", default="")

    return render_template(
        "blast-promo.html",
        form=form,
        campaign_id=campaign_id,
        referral_id=referral_id,
        installment_period="yearly",
        key=app.config["STRIPE_KEYS"]["publishable_key"],
        bundles=bundles,
    )


@app.route("/submit-blast-promo", methods=["POST"])
def submit_blast_promo():
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
        return render_template("error.html", message=message, bundles=bundles)
    if form.validate():
        app.logger.info("----Adding Blast subscription...")
        add_blast_subscription.delay(customer=customer, form=clean(request.form))
        gtm = {"event_value": "200", "event_label": "annual discounted"}
        return render_template("blast-charge.html", bundles=bundles, gtm=gtm)
    else:
        app.logger.error("Failed to validate form")
        message = "There was an issue saving your donation information."
        return render_template("error.html", message=message, bundles=bundles)


@app.route("/blastform")
def the_blast_form():
    bundles = get_bundles("old")
    form = BlastForm()
    if request.args.get("amount"):
        amount = request.args.get("amount")
    else:
        amount = 349
    installment_period = request.args.get("installmentPeriod")

    campaign_id = request.args.get("campaignId", default="")
    referral_id = request.args.get("referralId", default="")

    return render_template(
        "blast-form.html",
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
    bundles = get_bundles("old")
    app.logger.info(pformat(request.form))
    form = BlastForm(request.form)

    email_is_valid = validate_email(request.form["stripeEmail"])
    amount = request.form["amount"]

    if email_is_valid:
        customer = stripe.Customer.create(
            email=request.form["stripeEmail"], card=request.form["stripeToken"]
        )
        app.logger.info(f"Customer id: {customer.id}")
    else:
        message = "There was an issue saving your email address."
        return render_template("error.html", message=message, bundles=bundles)
    if form.validate():
        app.logger.info("----Adding Blast subscription...")
        add_blast_subscription.delay(customer=customer, form=clean(request.form))

        if amount == "349":
            event_label = "annual"
        elif amount == "40":
            event_label = "monthly"
        elif amount == "325":
            event_label = "annual tax exempt"

        gtm = {"event_value": amount, "event_label": event_label}

        return render_template("blast-charge.html", bundles=bundles, gtm=gtm)
    else:
        app.logger.error("Failed to validate form")
        message = "There was an issue saving your donation information."
        return render_template("error.html", message=message, bundles=bundles)


@app.route("/error")
def error():
    bundles = get_bundles("old")
    message = "Something went wrong!"
    return render_template("error.html", message=message, bundles=bundles)


@app.errorhandler(404)
def page_not_found(error):
    bundles = get_bundles("old")
    message = "The page you requested can't be found."
    return render_template("error.html", message=message, bundles=bundles), 404


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

    app.logger.info(payload)

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

    if event.type == "customer.source.updated":
        customer_source_updated.delay(event)

    # TODO change this to debug later
    app.logger.info(event)

    return "", 200


def add_opportunity(contact=None, form=None, customer=None):
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


def add_circle_membership(contact=None, form=None, customer=None):

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
    rdo.open_ended_status = "None"

    apply_card_details(rdo=rdo, customer=customer)
    rdo.save()

    return rdo


def add_recurring_donation(contact=None, form=None, customer=None):
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
    rdo.open_ended_status = "Open"

    apply_card_details(rdo=rdo, customer=customer)
    rdo.save()

    return rdo


def add_business_rdo(account=None, form=None, customer=None):
    """
    Adds a recurring business membership to Salesforce.
    """

    if form["installment_period"] is None:
        raise Exception("installment_period must have a value")

    year = datetime.now(tz=ZONE).strftime("%Y")

    rdo = RDO(account=account)
    rdo.name = f"{year} Business {account.name} Recurring"
    rdo.type = "Business Membership"
    rdo.record_type_name = "Business Membership"
    rdo.stripe_customer = customer["id"]
    rdo.campaign_id = form["campaign_id"]
    rdo.referral_id = form["referral_id"]
    rdo.description = "Texas Tribune Business Membership"
    rdo.agreed_to_pay_fees = form["pay_fees_value"]
    rdo.encouraged_by = form["reason"]
    rdo.lead_source = "Stripe"
    rdo.amount = form.get("amount", 0)
    rdo.installments = None
    rdo.open_ended_status = "Open"
    rdo.installment_period = form["installment_period"]

    apply_card_details(rdo=rdo, customer=customer)
    rdo.save()

    return rdo


@celery.task(name="app.add_business_membership")
def add_business_membership(
    form=None, customer=None, donation_type="business_membership"
):
    """
    Adds a business membership. Both single and recurring.

    It will look for a matching Contact (or create one). Then it will look for a
    matching Account (or create one). Then it will add the single or recurring donation
    to the Account. Then it will add an Affiliation to link the Contact with the
    Account. It sends a notification to Slack (if configured). It will send email
    notification about the new membership.

    """

    form = clean(form)

    first_name = form["first_name"]
    last_name = form["last_name"]
    email = form["stripeEmail"]

    website = form["website"]
    business_name = form["business_name"]
    shipping_city = form["shipping_city"]
    shipping_street = form["shipping_street"]
    shipping_state = form["shipping_state"]
    shipping_postalcode = form["shipping_postalcode"]

    logging.info("----Getting contact....")
    contact = Contact.get_or_create(
        email=email, first_name=first_name, last_name=last_name
    )
    if contact.work_email is None:
        contact.work_email = email
        contact.save()
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

    logging.info("----Getting account....")

    account = Account.get_or_create(
        record_type_name="Organization",
        website=website,
        name=business_name,
        shipping_street=shipping_street,
        shipping_city=shipping_city,
        shipping_state=shipping_state,
        shipping_postalcode=shipping_postalcode,
    )
    logging.info(account)

    if form["installment_period"] not in ["yearly", "monthly"]:
        raise Exception("Business membership must be either yearly or monthly")

    logging.info("----Creating recurring business membership...")
    rdo = add_business_rdo(account=account, form=form, customer=customer)
    logging.info(rdo)
    # get opportunities
    opportunities = rdo.opportunities()
    today = datetime.now(tz=ZONE).strftime("%Y-%m-%d")
    opp = [
        opportunity
        for opportunity in opportunities
        if opportunity.expected_giving_date == today
    ][0]
    charge(opp)
    notify_slack(account=account, contact=contact, rdo=rdo)

    logging.info("----Getting affiliation...")

    affiliation = Affiliation.get_or_create(
        account=account, contact=contact, role="Business Member Donor"
    )
    logging.info(affiliation)

    send_email_new_business_membership(account=account, contact=contact)

    if contact.duplicate_found:
        send_multiple_account_warning(contact)

    return True


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
    rdo.open_ended_status = "Open"
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
    charge(opp)

    return True


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
