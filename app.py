import os
import stripe
from flask import Flask, render_template, request
from salesforce import add_opportunity
from salesforce import add_recurring_donation
from salesforce import upsert
from config import stripe_keys, FLASK_SECRET_KEY
from forms import DonateForm

from pprint import pprint

from sassutils.wsgi import SassMiddleware

stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__)

app.secret_key = FLASK_SECRET_KEY

app.wsgi_app = SassMiddleware(app.wsgi_app, {
        'app': ('static/sass', 'static/css', 'static/css')
    })

@app.route('/memberform')
def member_form():
    form = DonateForm()
    amount = request.args.get('amount')
    return render_template('member-form.html', form=form, key=stripe_keys['publishable_key'])


@app.route('/donateform')
def donate_renew_form():
    form = DonateForm()
    return render_template('donate-form.html', form=form, key=stripe_keys['publishable_key'])


@app.route('/circleform')
def circle_form():
    form = DonateForm()
    return render_template('circle-form.html', form=form, key=stripe_keys['publishable_key'])


@app.route('/error')
def error():
    message = "Something went wrong!"
    return render_template('error.html', message=message)


# create customer in Stripe
# get or create payer in Salesforce - add Stripe Customer Id
# create opportunity or recurring donation object

@app.route('/charge', methods=['POST'])
def charge():


    pprint ('Request: {}'.format(request))

    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        card=request.form['stripeToken']
    )
    #print ('Customer: {}'.format(customer))
    upsert(request=request, customer=customer)

    #charge = stripe.Charge.create(
    #   customer=customer.id,
    #   amount=int(request.form['Opportunity.Amount']) * 100,
    #   currency='usd',
    #   description='Change Me' # TODO
    #)
    # except stripe.error.CardError, e:
    # The card has been declined
    #print ('Charge: {}'.format(charge))
    if (request.form['InstallmentPeriod'] == 'None'):
        print("----One time payment...")
        add_opportunity(request=request, customer=customer)
    else:
        print("----Recurring payment...")
        add_recurring_donation(request=request, customer=customer)

    return render_template('charge.html', amount=request.form['Opportunity.Amount'])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
