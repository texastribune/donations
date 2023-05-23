#! /bin/bash
echo "3, 2, 1, let's jam..."
sh -c "npm run dev \
    & flask --app server run --host=0.0.0.0 \
    & C_FORCE_ROOT=True celery -A server.app.celery worker --without-heartbeat --without-gossip --without-mingle --loglevel=INFO"
