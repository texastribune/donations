Donations
=========

Software to collect donations for nonprofits. It integrates with Salesforce, Stripe, Amazon Pay, Slack and Sentry.

- Python running Flask
- supports single and recurring donations
- easily deployed on Heroku

Getting Started
---------------

The recommended method for running this repo locally is to use [Docker](https://www.docker.com/). If you don't already have Docker set up, you'll want to [install Docker for Mac](https://docs.docker.com/engine/installation/mac/) to get a Docker environment set up on your computer.

You'll also need to have an `env` file set up with the environment variables for Stripe
and Salesforce so that Docker can find them. By default the `Makefile` will look for
`env-docker` but this can be overridden with the `DOCKER_ENV_FILE` environment variable.

You should also install [`pre-commit`](https://pre-commit.com/#install), which we use for managing Git hooks (including JS formatting via [Prettier](https://prettier.io/)). Once downloaded, run `pre-commit install` at the root of this repo. You'll also need Node version 12.

Requirements
------------

Python 3.6+
See requirements.txt and dev-requirements.txt for specific Python packages and versions.

Environment
-----------

| Variable                    |                                        Example |
|-----------------------------|-----------------------------------------------:|
| `FLASK_SECRET_KEY`          |  b'f;\xeb\x9bT2\xcd\xdb\xe1#z\xfb\xab\xf8(\x03'|
| `PUBLISHABLE_KEY`           |                                  pk_test_12345 |
| `SECRET_KEY`                |                                  sk_test_12335 |
| `LOG_LEVEL`                 |                                          DEBUG |
| `AUTH0_PORTAL_M2M_CLIENT_ID`|                                         string |
| `AUTH0_PORTAL_M2M_CLIENT_SECRET`|                                     string |
| `AUTH0_DOMAIN`              |                                     domain.com |
| `AUTH0_PORTAL_AUDIENCE`     |                                      foobarbaz |
| `AUTH0_PORTAL_CLIENT_ID`    |                             stringstringstring |
| `ENABLE_PORTAL`             |                                           True |
| `PORTAL_API_DOMAIN`         |                          <https://foo.bar/api> |
| `PORTAL_CAMPAIGN_ID`        |                             stringstringstring |
| `SALESFORCE_HOST`           |                            test.salesforce.com |
| `SALESFORCE_CLIENT_ID`      |                                                |
| `SALESFORCE_CLIENT_SECRET`  |                                                |
| `SALESFORCE_USERNAME`       |                                                |
| `SALESFORCE_PASSWORD`       |                                                |
| `SALESFORCE_TOKEN`          |                                                |
| `SALESFORCE_API_VERSION`    |                                          v43.0 |
| `CELERY_BROKER_URL`         |              amqp://guest:guest@rabbitmq:5672/ |
| `CELERY_RESULT_BACKEND`     |                           redis://redis:6379/0 |
| `CELERY_ALWAYS_EAGER`       |                                          False |
| `CELERY_TASK_SERIALIZER`    |                                           json |
| `ENABLE_SENTRY`             |                                           True |
| `ENABLE_SENTRY_RELEASE`     |                                           True |
| `SENTRY_ENVIRONMENT`        |                                           test |
| `SENTRY_DSN`                |        <https://user:pass@sentry/7?timeout=10> |
| `SENTRY_AUTH_TOKEN`         |                                                |
| `SENTRY_ORG`                |                                       your-org |
| `SENTRY_PROJECT`            |                                      donations |
| `ENABLE_SLACK`              |                                          False |
| `SLACK_API_KEY`             |                                                |
| `SLACK_CHANNEL`             |                                     #donations |
| `SLACK_CHANNEL_CANCELLATIONS` |                           #bot-cancellations |
| `SLACK_CIRCLE_NOTIFICATIONS`|                               #circle-failures |
| `DEFAULT_MAIL_SENDER`       |                                    foo@bar.org |
| `MAIL_SERVER`               |                                mail.server.com |
| `MAIL_USERNAME`             |                                                |
| `MAIL_PASSWORD`             |                                                |
| `MAIL_PORT`                 |                                             25 |
| `MAIL_USE_TLS`              |                                           True |
| `ACCOUNTING_MAIL_RECIPIENT` |                                    foo@bar.org |
| `BUSINESS_MEMBER_RECIPIENT` |                                    foo@bar.org |
| `CIRCLE_FAILURE_RECIPIENT`  |                                    foo@bar.org |
| `REDIS_URL`                 |                             redis://redis:6379 |
| `REPORT_URI`                |                              <https://foo.bar> |
| `RECAPTCHA_SECRET_KEY`      |                             stringstringstring |
| `RECAPTCHA_SITE_KEY`        |                             stringstringstring |
| `BAD_ACTOR_API_URL`         |                          <https://foo.bar.api> |
| `BAD_ACTOR_NOTIFICATION_URL`|                          <https://foo.bar.api> |

Running the Project
-------------------

Run `make`. This simple command file does a few things...
* spins up RabbitMQ and Redis containers that we connect to
* starts the flask app via the initializer in server.app
* builds CSS and JS files in watch mode

After all of this runs, you can interact with the app at `localhost:80`

NOTE: If you are a Tribune engineer, you may need to use `local.texastribune.org/donate` in order to sign in to your account or otherwise interact with the account page.

Running tests
-------------

To run the project tests, run
`make test`

Project Structure
-----------------

Though flask is pretty unopinionated about project structure, we've opted to use a "simple package" approach to our structure as mentioned as a possible option in the [flask documentation](https://flask.palletsprojects.com/en/2.3.x/patterns/packages/#simple-packages). Thus, the flasky pieces of this project live in the `server` folder. This ends up adhering closest to the current structure of our other major project, creating some consistentcy.

Security
--------

If you find vulnerabilities in this repo please report them to security@texastribune.org.
