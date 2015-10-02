import os
from flask import Flask, render_template, request
import stripe
from salesforce import add_opportunity
from salesforce import add_recurring_donation

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


@app.route('/error')
def error():
    message = "Something went wrong!"
    return render_template('error.html', message=message)


@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = request.form['Opportunity.Amount']
#    description = request.form['Description']

    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        card=request.form['stripeToken']
    )

    print ('Customer: {}'.format(customer))

    charge = stripe.Charge.create(
       customer=customer.id,
       amount=int(amount) * 100,
       currency='usd',
       description='Change Me' # TODO
    )

    print ('Charge: {}'.format(charge))

    if (request.form['frequency'] == 'one-time'):
        add_opportunity(request=request.form, customer=customer, charge=charge,
                reason="I heart the Trib!") # TODO
    else:
        add_recurring_donation(request=request.form, customer=customer, charge=charge,
                reason="I love the Trib!") #TODO

    return render_template('charge.html', amount=amount)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
