#!/usr/bin/env bash
# exit on error

pip install -r requirements.txt

python manage.py collectstatic --noinput