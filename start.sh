#!/bin/bash
python manage.py collectstatic --noinput &&
python manage.py migrate &&
gunicorn luoyangc.wsgi:application -c gunicorn.conf