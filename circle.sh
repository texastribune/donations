#!/usr/bin/env bash

npm run lint || exit 1
python -m pytest "tests" --cov=/app
