web: gunicorn app:app --log-file=-
worker: celery -A app.celery worker --beat --loglevel=INFO
