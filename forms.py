from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import (
    BooleanField,
    DecimalField,
    HiddenField,
    RadioField,
    StringField,
)
from wtforms.fields.html5 import EmailField


# amount must be $1 or higher
def validate_amount(form, field):
    value = field.data
    if value is None:
        raise validators.ValidationError("Non-numeric amount provided")
    if value < 1:
        raise validators.ValidationError("Amount is less than 1")


# if value starts with a dollar sign, remove it
# then convert to a float
def format_amount(value):
    if value.startswith("$"):
        value = value[1:]
    try:
        return float(value)
    except ValueError:
        return None


def strip_whitespace(value):
    if value is not None and hasattr(value, "strip"):
        return value.strip()
    return value


class BaseForm(FlaskForm):
    class Meta:
        def bind_field(self, form, unbound_field, options):
            filters = unbound_field.kwargs.get("filters", [])
            filters.append(strip_whitespace)
            return unbound_field.bind(form=form, filters=filters, **options)

    first_name = StringField(
        "First name", [validators.required(message="Your first name is required.")]
    )
    last_name = StringField(
        "Last name", [validators.required(message="Your last name is required.")]
    )
    amount = StringField(
        "Amount",
        validators=[
            validators.required(message="Please choose a donation amount."),
            validate_amount,
        ],
        filters=[format_amount],
    )
    stripeEmail = EmailField(
        "Email address", [validators.DataRequired(), validators.Email()]
    )
    stripeToken = HiddenField("Stripe token", [validators.InputRequired()])
    recaptchaToken = HiddenField("Recaptcha token", [validators.InputRequired()])
    description = HiddenField("Description", [validators.InputRequired()])
    pay_fees_value = HiddenField(
        "Pay Fees Value", [validators.AnyOf(["True", "False"])]
    )
    reason = StringField("Encouraged to give by", [validators.Length(max=255)])
    campaign_id = HiddenField("Campaign ID")
    referral_id = HiddenField("Referral ID")


class DonateForm(BaseForm):
    installment_period = StringField(
        "Installment Period", [validators.AnyOf(["yearly", "monthly", "None"])]
    )
    zipcode = StringField("ZIP Code", [validators.Length(max=5)])


class CircleForm(BaseForm):
    installment_period = StringField(
        "Installment Period", [validators.AnyOf(["yearly", "monthly"])]
    )
    zipcode = StringField("ZIP Code", [validators.Length(max=5)])


class BusinessMembershipForm(BaseForm):
    website = StringField("Web site", [validators.URL(), validators.Length(max=255)])
    business_name = StringField(
        "Business name", [validators.InputRequired(), validators.Length(max=255)]
    )
    shipping_city = StringField("Shipping City", [validators.Length(max=40)])
    shipping_state = StringField("Shipping State", [validators.Length(max=2)])
    shipping_street = StringField("Shipping Street", [validators.Length(max=255)])
    shipping_postalcode = StringField("ZIP Code", [validators.Length(max=20)])
    installment_period = StringField([validators.AnyOf(["yearly", "monthly"])])


class BlastForm(FlaskForm):
    first_name = StringField(
        "First name", [validators.required(message="Your first name is required.")]
    )
    last_name = StringField(
        "Last name", [validators.required(message="Your last name is required.")]
    )
    amount_choices = [
        ("349", "Annual"),
        ("40", "Monthly"),
        ("325", "Annual Tax-Exempt"),
    ]
    amount = RadioField("Amount", choices=amount_choices, default="349")
    subscriber_email = EmailField(
        "Subscriber Email address", [validators.DataRequired(), validators.Email()]
    )
    installment_period = HiddenField("Installment Period")
    campaign_id = HiddenField("Campaign ID")
    referral_id = HiddenField("Referral ID")
    description = HiddenField("Description")
    pay_fees = BooleanField("Agree to pay fees")
    pay_fees_value = HiddenField("Pay Fees Value")


class BlastPromoForm(FlaskForm):
    first_name = StringField(
        "First name", [validators.required(message="Your first name is required.")]
    )
    last_name = StringField(
        "Last name", [validators.required(message="Your last name is required.")]
    )
    subscriber_email = EmailField(
        "Subscriber Email address", [validators.DataRequired(), validators.Email()]
    )
    installment_period = HiddenField("Installment Period")
    campaign_id = HiddenField("Campaign ID")
    referral_id = HiddenField("Referral ID")
    description = HiddenField("Description")
    pay_fees = BooleanField("Agree to pay fees")
    pay_fees_value = HiddenField("Pay Fees Value")
