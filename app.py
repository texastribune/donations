import os
from flask import Flask, render_template, request
import stripe
from salesforce import SalesforceConnection

stripe_keys = {
    'secret_key': os.environ['SECRET_KEY'],
    'publishable_key': os.environ['PUBLISHABLE_KEY']
}
stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__)

@app.route('/form')
def checkout_form():
    amount = request.args.get('amount')
    return render_template('form.html', key=stripe_keys['publishable_key'])


@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = int(request.form['amount']) * 100

    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        card=request.form['stripeToken']
    )
    # grab the last four of card #
    last_four = customer.sources.data[0].last4

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Change Me'
    )
    sf = SalesforceConnection()
    account_id = sf.get_contact(request.form['stripeEmail'])
    foo = sf.add_opp(account_id, amount, )

    return render_template('charge.html', amount=amount)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
