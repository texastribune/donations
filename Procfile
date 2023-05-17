web: gunicorn server.app:app --log-file=-
worker: celery -A app.celery worker --without-heartbeat --without-gossip --without-mingle --beat --loglevel=$LOG_LEVEL
