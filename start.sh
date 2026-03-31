#!/bin/sh
python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec gunicorn offnotes.wsgi:application --bind :$PORT --workers 2
