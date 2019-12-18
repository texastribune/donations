from celery import Celery
from config import SENTRY_DSN


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker_pool_limit=1,
        broker_heartbeat=None,
        broker=app.config["CELERY_BROKER_URL"],
        broker_connection_timeout=30,
        result_backend=None,
        event_queue_expires=60,
        worker_prefetch_multiplier=1,
        worker_log_format="%(levelname)s %(name)s/%(module)s:%(lineno)d - %(message)s",
        worker_task_log_format="%(levelname)s %(name)s/%(module)s:%(lineno)d - %(message)s",
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
