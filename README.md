Stripe-Salesforce
=================

This repo integrates [Stripe Checkout](https://stripe.com/docs/checkout) and [Salesforce](http://www.salesforce.com/) into our [donations app](http://support.texastribune.org/).

Getting Started
---------------

The recommended method for running this repo locally is to use [Docker](https://www.docker.com/). 

You'll need to have an `env` file set up with the environment variables for Stripe and Salesforce so that Docker can find them.

Running the Project
-------------------

Run `make interactive`. This will drop you into the Flask app.

Run `python3 app.py`. You should then be able to interact with the app at `docker.local` (or whatever you set Docker to resolve to).

### Tests

Running tests
-------------


