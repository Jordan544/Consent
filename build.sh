#!/usr/bin/env bash
# Exit on error
set -o errexit

cd finalyearproject

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate