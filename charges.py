import stripe


class ChargeException(Exception):
    pass


def charge_customer(customer_id, amount, description):
    """
    Charge a customer.

    Stripe wants the amount in cents so we multiply by 100.
    """

    print('---- Charging ${} to {} ({})'.format(amount, customer_id,
        description))

    amount = amount * 100

    try:
        charge = stripe.Charge.create(
                customer=customer_id,
                amount=amount,
                currency='usd',
                description=description,
                )
    except stripe.error.CardError as e:
        # look for decline code:
        error = e.json_body['error']
        print('The card has been declined:')
        print('\tStatus: {}'.format(e.http_status))
        print('\tType: {}'.format(error.get('type', '')))
        print('\tCode: {}'.format(error.get('code', '')))
        print('\tParam: {}'.format(error.get('param', '')))
        print('\tMessage: {}'.format(error.get('message', '')))
        print('\tDecline code: {}'.format(error.get('decline_code', '')))
        raise ChargeException(error.get('message'))
    except Exception as e:
        print('Problem: {}'.format(e))
        raise e

    print(charge.outcome.seller_message)
    return charge
