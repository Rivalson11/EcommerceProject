#!/bin/bash

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start Celery worker and beat services
celery -A ecommerce worker --loglevel=info &
celery -A ecommerce beat --loglevel=info &
