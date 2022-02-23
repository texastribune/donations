web: newrelic-admin run-program gunicorn app:app --log-file=-
worker: newrelic-admin run-program celery -A app.celery worker --without-heartbeat --without-gossip --without-mingle --beat --loglevel=$LOG_LEVEL
