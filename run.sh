#!/usr/bin/env bash

gunicorn server:app -k gevent --timeout 500 -b "0.0.0.0:8000"
