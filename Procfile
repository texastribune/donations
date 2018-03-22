web: gunicorn app:app --log-file=-
worker: celery -A app.celery worker --loglevel=INFO
