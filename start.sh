#!/bin/bash
python manage.py collectstatic --noinput &&
python manage.py migrate &&
gunicorn config.wsgi:application -c gunicorn.conf