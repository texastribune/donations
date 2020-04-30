#!/usr/bin/env bash

npm run lint || exit 1
python /usr/local/bin/py.test /app/tests.py --cov=/app
