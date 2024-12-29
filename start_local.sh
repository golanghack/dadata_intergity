#!/usr/bin/env bash

wait-for-it "$DB_HOST:5432" -t 10

python3 manage.py collectstatic --noinput
python3 manage.py makemigrations 
python3 manage.py migrate
python3 manage.py csu
python3 manage.py health_check
gunicorn config.wsgi:application --bind 0.0.0.0:8001