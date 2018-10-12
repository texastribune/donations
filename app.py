"""
This file is the entrypoint for this Flask application. Can be executed with 'flask run', 'python app.py' or via a WSGI server like gunicorn or uwsgi.
"""
import json
import locale
import logging
import os
from config import FLASK_DEBUG, FLASK_SECRET_KEY, TIMEZONE, LOG_LEVEL
from datetime import datetime

from pytz import timezone

import celery
import stripe
from app_celery import make_celery
from flask import Flask, redirect, render_template, request, send_from_directory
from forms import BlastForm, DonateForm, BusinessMembershipForm, CircleForm
from npsp import RDO, Contact, Opportunity, Affiliation, Account
from raven.contrib.flask import Sentry
from sassutils.wsgi import SassMiddleware
from util import (
    clean,
    notify_slack,
    send_multiple_account_warning,
    send_email_new_business_membership,
)
from validate_email import validate_email

ZONE = timezone(TIMEZONE)

locale.setlocale(locale.LC_ALL, "C")

app = Flask(__name__)

log_level = logging.getLevelName(LOG_LEVEL)
app.logger.setLevel(log_level)

app.secret_key = FLASK_SECRET_KEY

app.wsgi_app = SassMiddleware(
    app.wsgi_app, {"app": ("static/sass", "static/css", "static/css")}
)

app.config.from_pyfile("config.py")
app.config.update(
    CELERY_ACCEPT_CONTENT=["pickle", "json"],
    CELERY_ALWAYS_EAGER=False,
    CELERY_IMPORTS=("app", "npsp", "batch"),
)
stripe.api_key = app.config["STRIPE_KEYS"]["secret_key"]

make_celery(app)


if app.config["ENABLE_SENTRY"]:
    sentry = Sentry(app, dsn=app.config["SENTRY_DSN"])

"""
Redirects, including for URLs that used to be
part of the old donations app that lived at
support.texastribune.org.
"""


@app.route("/blast-vip")
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
def circle_html_route():
    return redirect("/circleform", code=302)


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
    if FLASK_DEBUG:
        build_dir = os.path.join("static", "build")
        asset_path = "/static/build/"
    else:
        build_dir = os.path.join(root_dir, "app", "static", "prod")
        asset_path = "/static/prod/"
    bundles = {"css": [], "js": []}
    manifest_path = os.path.join(build_dir, "assets.json")
    with open(manifest_path) as manifest:
        assets = json.load(manifest)
    entrypoint = assets["entrypoints"][entry]
    for bundle in entrypoint["js"]:
        bundles["js"].append(asset_path + bundle)
    for bundle in entrypoint["css"]:
        bundles["css"].append(asset_path + bundle)
    return bundles


@celery.task(name="app.add_donation")
def add_donation(form=None, customer=None):
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

    if period is None:
        logging.info("----Creating one time payment...")
        opportunity = add_opportunity(contact=contact, form=form, customer=customer)
        logging.info(opportunity)
        notify_slack(contact=contact, opportunity=opportunity)
    else:
        logging.info("----Creating recurring payment...")
        rdo = add_recurring_donation(contact=contact, form=form, customer=customer)
        logging.info(rdo)
        notify_slack(contact=contact, rdo=rdo)

    if contact.duplicate_found:
        send_multiple_account_warning(contact)

    return True


def do_charge_or_show_errors(template, bundles, function):
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
    logging.info(customer.id)
    function(customer=customer, form=clean(request.form))
    gtm = {
        "event_value": amount,
        "event_label": "once" if installment_period == "None" else installment_period,
    }
    return render_template("charge.html", gtm=gtm, bundles=get_bundles("charge"))


def validate_form(FormType, bundles, template, function=add_donation.delay):
    app.logger.info(request.form)

    form = FormType(request.form)
    email = request.form["stripeEmail"]

    if not validate_email(email):
        message = "There was an issue saving your email address."
        return render_template("error.html", message=message)
    if not form.validate():
        app.logger.warning(f"Form validation errors: {form.errors}")
        message = "There was an issue saving your donation information."
        return render_template("error.html", message=message)

    return do_charge_or_show_errors(
        bundles=bundles, template=template, function=function
    )


@app.route("/donate", methods=["GET", "POST"])
def member2_form():
    bundles = get_bundles("donate")
    template = "member-form2.html"

    if request.method == "POST":
        return validate_form(DonateForm, bundles=bundles, template=template)

    return render_template(
        template, bundles=bundles, key=app.config["STRIPE_KEYS"]["publishable_key"]
    )


@app.route("/circleform", methods=["GET", "POST"])
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


@app.route("/blastform")
def the_blast_form():
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
        openended_status="Open",
        amount=amount,
        key=app.config["STRIPE_KEYS"]["publishable_key"],
    )


@app.route("/submit-blast", methods=["POST"])
def submit_blast():

    app.logger.info(request.form)
    form = BlastForm(request.form)

    email_is_valid = validate_email(request.form["stripeEmail"])

    if email_is_valid:
        customer = stripe.Customer.create(
            email=request.form["stripeEmail"], card=request.form["stripeToken"]
        )
        app.logger.info(customer.id)
    else:
        message = "There was an issue saving your email address."
        return render_template("error.html", message=message)
    if form.validate():
        app.logger.info("----Adding Blast subscription...")
        add_blast_subscription.delay(customer=customer, form=clean(request.form))
        return render_template("blast-charge.html")
    else:
        app.logger.warning("Failed to validate form")
        message = "There was an issue saving your donation information."
        return render_template("error.html", message=message)


@app.route("/error")
def error():
    message = "Something went wrong!"
    return render_template("error.html", message=message)


@app.errorhandler(404)
def page_not_found(error):
    message = "The page you requested can't be found."
    return render_template("error.html", message=message), 404


@app.route("/.well-known/apple-developer-merchantid-domain-association")
def merchantid():
    """
    This is here to verify our domain so Stripe can support Apple Pay.
    """
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(
        os.path.join(root_dir, "app"), "apple-developer-merchantid-domain-association"
    )


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

    opportunity.save()
    return opportunity


def add_recurring_donation(contact=None, form=None, customer=None):
    """
    This will add a recurring donation to Salesforce. Both Circle and regular.
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

    installments = form["installments"]

    open_ended_status = form["openended_status"]
    installment_period = form["installment_period"]
    rdo.open_ended_status = open_ended_status
    rdo.installments = installments
    rdo.installment_period = installment_period

    if (
        open_ended_status is None
        and (installments == 3 or installments == 36)
        and (installment_period == "yearly" or installment_period == "monthly")
    ):
        rdo.type = "Giving Circle"
        rdo.description = "Texas Tribune Circle Membership"

    rdo.save()
    return rdo


def add_business_opportunity(account=None, form=None, customer=None):
    """
    Adds a single business membership to Salesforce.
    """

    year = datetime.now(tz=ZONE).strftime("%Y")
    opportunity = Opportunity(account=account)
    opportunity.record_type_name = "Business Membership"
    opportunity.name = f"{year} Business {account.name} One time"
    opportunity.amount = form.get("amount", 0)
    opportunity.stripe_customer = customer["id"]
    opportunity.campaign_id = form["campaign_id"]
    opportunity.referral_id = form["referral_id"]
    opportunity.description = "Texas Tribune Business Membership"
    opportunity.agreed_to_pay_fees = form["pay_fees_value"]
    opportunity.encouraged_by = form["reason"]
    opportunity.lead_source = "Stripe"
    opportunity.save()
    return opportunity


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
    rdo.installments = form["installments"]
    rdo.open_ended_status = form["openended_status"]
    rdo.installment_period = form["installment_period"]
    rdo.save()
    return rdo


@celery.task(name="app.add_business_membership")
def add_business_membership(form=None, customer=None):
    """
    Adds a business membership. Both single and recurring.

    It will look for a matching Contact (or create one). Then it will look for a matching Account (or create one). Then it will add the single or recurring donation to the Account. Then it will add an Affiliation to link the Contact with the Account. It sends a notification to Slack (if configured). It will send email notification about the new membership.
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

    if form["installment_period"] is None:
        logging.info("----Creating single business membership...")
        opportunity = add_business_opportunity(
            account=account, form=form, customer=customer
        )
        logging.info(opportunity)
        notify_slack(account=account, opportunity=opportunity)
    else:
        logging.info("----Creating recurring business membership...")
        rdo = add_business_rdo(account=account, form=form, customer=customer)
        logging.info(rdo)
        notify_slack(account=account, rdo=rdo)

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
    Adds a Blast subscription. Blast subscriptions are always recurring. They have two email addresses: one for billing and one for the newsletter subscription.
    """

    form = clean(form)
    logging.info(form)

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
    if rdo.amount == 40:
        rdo.installment_period = "monthly"
    else:
        rdo.installment_period = "yearly"
    now = datetime.now(tz=ZONE).strftime("%Y-%m-%d %I:%M:%S %p %Z")
    rdo.name = f"{first_name} {last_name} - {now} - The Blast"
    rdo.type = "The Blast"
    rdo.billing_email = form["stripeEmail"]
    rdo.blast_subscription_email = form["subscriber_email"]

    logging.info("----Saving RDO....")
    rdo.save()
    logging.info(rdo)

    return True


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
