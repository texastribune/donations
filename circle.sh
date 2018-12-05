#!/usr/bin/env bash

# yarn lint || exit 1
python texastribune/checkout:dev /usr/local/bin/py.test /app/tests.py --cov=/app
