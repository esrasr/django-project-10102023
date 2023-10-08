#!/bin/sh
echo "Starting Django Collectstatic..."
python manage.py collectstatic --noinput
echo "Starting Django Migration..."
python manage.py migrate 
echo "Starting Django Application..."
exec "$@"