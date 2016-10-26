from flask_wtf import Form

from wtforms.fields import StringField, HiddenField, BooleanField, DecimalField
from wtforms.fields import RadioField, SelectField
from wtforms import validators
from wtforms.fields.html5 import EmailField


class BaseForm(Form):
    first_name = StringField(u'First name',
        [validators.required(message="Your first name is required.")])
    last_name = StringField(u'Last name',
        [validators.required(message="Your last name is required.")])
    amount = DecimalField(u'Amount',
        [validators.required(message="Please choose a donation amount."),
        validators.NumberRange(min=1)])
    reason = StringField(u'Encouraged to contribute by')
    installment_period = HiddenField(u'Installment Period')
    installments = HiddenField(u'Installments')
    description = HiddenField(u'Description')
    pay_fees = BooleanField(u'Agree to pay fees')
    pay_fees_value = HiddenField(u'Pay Fees Value')


class MemberForm(BaseForm):
    openended_status = RadioField(u'Membership Duration',
        choices=[('Open', 'Sustaining'), ('None', 'One Year')],
        default='Open')


class DonateForm(BaseForm):
    openended_status = HiddenField(u'Openended Status')


class BlastForm(Form):
    first_name = StringField(u'First name',
        [validators.required(message="Your first name is required.")])
    last_name = StringField(u'Last name',
        [validators.required(message="Your last name is required.")])
    amount_choices = [
        ('349', 'Annual ($349)'),
        ('325', 'Annual Tax-Exempt ($325 — For government agencies and nonprofit organizations)'),
        ('40', 'Monthly ($40)'),
        ]
    amount = SelectField(u'Amount', choices=amount_choices)
    subscriber_email = EmailField('Subscriber Email address',
        [validators.DataRequired(), validators.Email()])
    installment_period = HiddenField(u'Installment Period')
    installments = HiddenField(u'Installments')
    openended_status = HiddenField(u'Openended Status')
    description = HiddenField(u'Description')
    pay_fees = BooleanField(u'Agree to pay fees')
    pay_fees_value = HiddenField(u'Pay Fees Value')
