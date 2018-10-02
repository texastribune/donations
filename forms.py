from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import (BooleanField, DecimalField, HiddenField,
                            RadioField, StringField)
from wtforms.fields.html5 import EmailField

class BaseForm(FlaskForm):
    first_name = StringField(u'First name',
        [validators.required(message="Your first name is required.")])
    last_name = StringField(u'Last name',
        [validators.required(message="Your last name is required.")])
    amount = DecimalField(u'Amount',
        [validators.required(message="Please choose a donation amount."),
        validators.NumberRange(min=1)])
    zipcode = StringField(u'ZIP Code', [validators.Length(max=5)])
    stripeEmail = EmailField('Email address',
        [validators.DataRequired(), validators.Email()])
    stripeToken = HiddenField(u'Stripe token', [validators.InputRequired()])
    description = HiddenField(u'Description', [validators.InputRequired()])
    pay_fees_value = HiddenField(u'Pay Fees Value',
        [validators.AnyOf(['True', 'False'])])
    reason = StringField(u'Encouraged to give by')
    campaign_id = HiddenField('Campaign ID')
    referral_id = HiddenField('Referral ID')

class DonateForm(BaseForm):
    installments = HiddenField(u'Installments', [validators.AnyOf(['None'])])
    openended_status = HiddenField(u'Openended Status',
        [validators.AnyOf(['None', 'Open'])])
    installment_period = StringField(u'Installment Period',
        [validators.AnyOf(['yearly', 'monthly', 'None'])])

class CircleForm(BaseForm):
    installments = HiddenField(u'Installments', [validators.AnyOf(['3', '36'])])
    openended_status = HiddenField(u'Openended Status', [validators.AnyOf(['None'])])
    installment_period = StringField(u'Installment Period',
        [validators.AnyOf(['yearly', 'monthly'])])

class BlastForm(FlaskForm):
    first_name = StringField(u'First name',
        [validators.required(message="Your first name is required.")])
    last_name = StringField(u'Last name',
        [validators.required(message="Your last name is required.")])
    amount_choices = [
        ('349', 'Annual'),
        ('40', 'Monthly'),
        ('325', 'Annual Tax-Exempt'),
    ]
    amount = RadioField(u'Amount', choices=amount_choices, default='349')
    subscriber_email = EmailField('Subscriber Email address',
        [validators.DataRequired(), validators.Email()])
    installment_period = HiddenField(u'Installment Period')
    installments = HiddenField(u'Installments')
    openended_status = HiddenField(u'Openended Status')
    campaign_id = HiddenField('Campaign ID')
    referral_id = HiddenField('Referral ID')
    description = HiddenField(u'Description')
    pay_fees = BooleanField(u'Agree to pay fees')
    pay_fees_value = HiddenField(u'Pay Fees Value')
