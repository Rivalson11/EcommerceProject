# Run migrations
python manage.py migrate

# Load fixture data
python manage.py loaddata your_app/fixtures/initial_data.json

# Collect static files
python manage.py collectstatic --noinput

# Start Celery and Django
celery -A ecommerce worker --loglevel=info &
celery -A ecommerce beat --loglevel=info &
python manage.py runserver 0.0.0.0:8000
