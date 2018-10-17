from celery import Celery
from raven import Client
from raven.contrib.celery import register_signal, register_logger_signal
from config import SENTRY_DSN
import logging

client = Client(SENTRY_DSN)

# register a custom filter to filter out duplicate logs
register_logger_signal(client)

# The register_logger_signal function can also take an optional argument
# `loglevel` which is the level used for the handler created.
# Defaults to `logging.ERROR`
register_logger_signal(client, loglevel=logging.INFO)

# hook into the Celery error handler
register_signal(client)

# The register_signal function can also take an optional argument
# `ignore_expected` which causes exception classes specified in Task.throws
# to be ignored
register_signal(client, ignore_expected=True)


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config["CELERY_BROKER_URL"])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
