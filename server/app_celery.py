import ssl
from celery import Celery
from .config import REDIS_URL, SENTRY_DSN


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker_pool_limit=1,
        broker_heartbeat=None,
        broker=app.config["CELERY_BROKER_URL"],
        broker_connection_timeout=60,
        redis_backend_use_ssl = {
            'ssl_cert_reqs': ssl.CERT_NONE,
        } if 'rediss' in REDIS_URL else {},
        result_backend=None,
        event_queue_expires=60,
        worker_prefetch_multiplier=1,
        worker_log_format="%(levelname)s %(name)s/%(module)s:%(lineno)d - %(message)s",
        worker_task_log_format="%(levelname)s %(name)s/%(module)s:%(lineno)d - %(message)s",
        worker_concurrency=3,
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

    def __call__(self, *args, **kwargs):
        with app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
