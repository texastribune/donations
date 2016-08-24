Stripe-Salesforce
=================

This repo integrates [Stripe Checkout](https://stripe.com/docs/checkout) and [Salesforce](http://www.salesforce.com/) into our [donations app](http://support.texastribune.org/).

Getting Started
---------------

The recommended method for running this repo locally is to use [Docker](https://www.docker.com/). If you don't already have Docker set up, you'll want to [install Docker Toolbox](https://www.docker.com/docker-toolbox) to get a Docker environment set up on your computer.

You'll also need to have an `env` file set up with the environment variables for Stripe and Salesforce so that Docker can find them.

Running the Project
-------------------

Run `make backing`. This will start RabbitMQ and Redis.
Run `make interactive`. This will drop you into the Flask app.

Run `python3 app.py`. You should then be able to interact with the app at `docker.local` (or whatever you set Docker to resolve to).
```
flower -A app.celery --port=5555 --address=0.0.0.0    # monitoring
C_FORCE_ROOT=True celery -A app.celery worker --loglevel=INFO &
celery beat --app app.celery &
gunicorn app:app --log-file=- --bind=0.0.0.0:5000 --access-logfile=-
```

### Tests

Running tests
-------------

To run the project tests, run
`make interactive`
`py.test tests.py`


### Deploy


If you're not invited to the Trib's Heroku group, get someone to invite you. Log in to Heroku on your console. Follow [Heroku instructions](https://devcenter.heroku.com/articles/git) for deploying. Specifically, you'll run the command `heroku git:remote -a stripe-prod` to set up your environment. Then deploy with the command `git push heroku master`.