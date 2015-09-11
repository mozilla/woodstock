#!/bin/bash

python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn woodstock.wsgi:application -b 0.0.0.0:8000 -w 2 --log-file -
