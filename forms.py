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


class DonateForm(FlaskForm):
    first_name = StringField(
        u"First name", [validators.required(message="Your first name is required.")]
    )
    last_name = StringField(
        u"Last name", [validators.required(message="Your last name is required.")]
    )
    amount = DecimalField(
        u"Amount",
        [
            validators.required(message="Please choose a donation amount."),
            validators.NumberRange(min=1),
        ],
    )
    reason = StringField(u"Encouraged to give by")
    zipcode = StringField(u"ZIP Code", [validators.Length(max=5)])
    campaign_id = HiddenField("Campaign ID")
    referral_id = HiddenField("Referral ID")
    installments = HiddenField(u"Installments")
    description = HiddenField(u"Description")
    pay_fees_value = HiddenField(u"Pay Fees Value")
    openended_status = HiddenField(u"Openended Status")
    customerId = HiddenField(u"Customer ID", [validators.InputRequired()])
    installment_period = RadioField(
        u"Installment Period",
        choices=[("yearly", "Yearly"), ("monthly", "Monthly"), ("None", "One Time")],
    )


class BlastForm(FlaskForm):
    first_name = StringField(
        u"First name", [validators.required(message="Your first name is required.")]
    )
    last_name = StringField(
        u"Last name", [validators.required(message="Your last name is required.")]
    )
    amount_choices = [
        ("349", "Annual"),
        ("40", "Monthly"),
        ("325", "Annual Tax-Exempt"),
    ]
    amount = RadioField(u"Amount", choices=amount_choices, default="349")
    subscriber_email = EmailField(
        "Subscriber Email address", [validators.DataRequired(), validators.Email()]
    )
    installment_period = HiddenField(u"Installment Period")
    installments = HiddenField(u"Installments")
    openended_status = HiddenField(u"Openended Status")
    campaign_id = HiddenField("Campaign ID")
    referral_id = HiddenField("Referral ID")
    description = HiddenField(u"Description")
    pay_fees = BooleanField(u"Agree to pay fees")
    pay_fees_value = HiddenField(u"Pay Fees Value")


class BusinessMembershipForm(FlaskForm):
    first_name = StringField(
        u"First name", [validators.required(message="Your first name is required.")]
    )
    last_name = StringField(
        u"Last name", [validators.required(message="Your last name is required.")]
    )
    amount = DecimalField(
        u"Amount",
        [
            validators.required(message="Please choose a donation amount."),
            validators.NumberRange(min=1),
        ],
    )
    website = StringField(u"Web site")
    business_name = StringField(u"Business name")
    reason = StringField(u"Encouraged to give by")
    zipcode = StringField(u"ZIP Code", [validators.Length(max=5)])
    campaign_id = HiddenField("Campaign ID")
    referral_id = HiddenField("Referral ID")
    installments = HiddenField(u"Installments")
    description = HiddenField(u"Description")
    pay_fees_value = HiddenField(u"Pay Fees Value")
    openended_status = HiddenField(u"Openended Status")
    customerId = HiddenField(u"Customer ID", [validators.InputRequired()])
    installment_period = RadioField(
        u"Installment Period",
        choices=[("yearly", "Yearly"), ("monthly", "Monthly"), ("None", "One Time")],
    )

