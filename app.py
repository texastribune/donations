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
from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
)
from forms import BlastForm, DonateForm, BusinessMembershipForm
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

zone = timezone(TIMEZONE)

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


@app.route("/donate")
def member2_form():
    bundles = get_bundles("donate")
    return render_template(
        "member-form2.html",
        bundles=bundles,
        key=app.config["STRIPE_KEYS"]["publishable_key"],
    )


@app.route("/circleform")
def circle_form():
    bundles = get_bundles("circle")
    return render_template(
        "circle-form.html",
        bundles=bundles,
        key=app.config["STRIPE_KEYS"]["publishable_key"],
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


@app.route("/create-customer", methods=["POST"])
def create_customer():
    stripe_email = request.json["stripeEmail"]
    email_is_valid = validate_email(stripe_email)

    if email_is_valid:
        try:
            customer = stripe.Customer.create(
                email=stripe_email, card=request.json["stripeToken"]
            )
            app.logger.info(customer.id)
            return jsonify({"customer_id": customer.id})
        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get("error", {})
            return (
                jsonify(
                    {
                        "expected": True,
                        "type": "card",
                        "message": err.get("message", ""),
                    }
                ),
                400,
            )
    else:
        message = """Our servers had an issue saving your email address.
                    Please make sure it's properly formatted. If the problem
                    persists, please contact inquiries@texastribune.org."""
        return jsonify({"expected": True, "type": "email", "message": message}), 400


@app.route("/charge", methods=["POST"])
def charge():

    app.logger.info(request.form)

    gtm = {}
    form = DonateForm(request.form)

    bundles = get_bundles("charge")

    if form.validate():
        try:
            app.logger.debug("----Retrieving Stripe customer...")
            customer = stripe.Customer.retrieve(request.form["customerId"])
            app.logger.info(customer.id)
            add_donation.delay(customer=customer, form=clean(request.form))
            if request.form["installment_period"] == "None":
                gtm["event_label"] = "once"
            else:
                gtm["event_label"] = request.form["installment_period"]
            gtm["event_value"] = request.form["amount"]
            return render_template(
                "charge.html", amount=request.form["amount"], gtm=gtm, bundles=bundles
            )
        except stripe.error.InvalidRequestError as e:
            body = e.json_body
            err = body.get("error", {})
            message = err.get("message", "")
            if "No such customer:" not in message:
                raise e
            else:
                app.logger.warning(message)
                return render_template("error.html", message=message)
    else:
        message = "There was an issue saving your donation information."
        app.logger.warning(f"Form validation errors: {form.errors}")
        return render_template("error.html", message=message)


@app.route("/bmcharge", methods=["POST"])
def bmcharge():

    app.logger.info(request.form)
    gtm = {}

    form = BusinessMembershipForm(request.form)

    bundles = get_bundles("charge")

    if form.validate():
        try:
            app.logger.info("----Retrieving Stripe customer...")
            customer = stripe.Customer.retrieve(request.form["customerId"])
            app.logger.info(customer.id)
            add_business_membership.delay(customer=customer, form=clean(request.form))
            if request.form["installment_period"] == "None":
                gtm["event_label"] = "once"
            else:
                gtm["event_label"] = request.form["installment_period"]
            gtm["event_value"] = request.form["amount"]
            return render_template(
                "charge.html", amount=request.form["amount"], gtm=gtm, bundles=bundles
            )
        except stripe.error.InvalidRequestError as e:
            body = e.json_body
            err = body.get("error", {})
            message = err.get("message", "")
            if "No such customer:" not in message:
                raise e
            else:
                app.logger.warning(message)
                return render_template("error.html", message=message)
    else:
        message = "There was an issue saving your donation information."
        app.logger.warning(f"Form validation errors: {form.errors}")
        return render_template("error.html", message=message)


@app.route("/.well-known/apple-developer-merchantid-domain-association")
def merchantid():
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(
        os.path.join(root_dir, "app"), "apple-developer-merchantid-domain-association"
    )


def add_opportunity(contact=None, form=None, customer=None):

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
    logging.info(opportunity)
    return opportunity


def add_recurring_donation(contact=None, form=None, customer=None):

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
    logging.info(rdo)

    return rdo


@celery.task(name="app.add_donation")
def add_donation(form=None, customer=None):
    """
    Add a contact and their donation into SF. This is done in the background
    because there are a lot of API calls and there's no point in making the
    payer wait for them.
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

    # intentionally overwriting zip but not name here

    if zipcode and not contact.created:
        contact.zipcode = zipcode
        contact.save()

    if period is None:
        logging.info("----Creating one time payment...")
        opportunity = add_opportunity(contact=contact, form=form, customer=customer)
        notify_slack(contact=contact, opportunity=opportunity)
    else:
        logging.info("----Creating recurring payment...")
        rdo = add_recurring_donation(contact=contact, form=form, customer=customer)
        notify_slack(contact=contact, rdo=rdo)

    if contact.duplicate_found:
        send_multiple_account_warning(contact)

    return True


def add_business_opportunity(account=None, form=None, customer=None):

    year = datetime.now(tz=zone).strftime("%Y")
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
    logging.info(opportunity)
    return opportunity


def add_business_rdo(account=None, form=None, customer=None):

    if form["installment_period"] is None:
        raise Exception("installment_period must have a value")

    year = datetime.now(tz=zone).strftime("%Y")

    rdo = RDO(account=account)
    rdo.name = f"{year} Business {account.name} Recurring"
    rdo.type = "Business Membership"
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
    logging.info(rdo)

    # since RDOs hardcode the Record Type to always be Membership we go change them here:
    # TODO do a composite update
    # maybe setting attr record_type_name on the RDO should trigger that?
    for opportunity in rdo.opportunities():
        opportunity.record_type_name = "Business Membership"
        opportunity.save()

    return rdo


@celery.task(name="app.add_business_membership")
def add_business_membership(form=None, customer=None):

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
        notify_slack(account=account, opportunity=opportunity)
    else:
        logging.info("----Creating recurring business membership...")
        rdo = add_business_rdo(account=account, form=form, customer=customer)
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
    now = datetime.now(tz=zone).strftime("%Y-%m-%d %I:%M:%S %p %Z")
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
