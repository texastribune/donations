from flask_wtf import Form

from wtforms.fields import StringField, IntegerField
from wtforms.validators import *

from flask import request

class DonateForm(Form):
    first_name = StringField(u'First')
    last_name = StringField(u'Last Name')
    amount = IntegerField(u'Amount')
    installment_period = StringField(u'Installment Period')
    installments = IntegerField(u'Installments')
    reason = StringField(u'Encouraged to contribute by')
    openended_status = StringField(u'Openended Status')
