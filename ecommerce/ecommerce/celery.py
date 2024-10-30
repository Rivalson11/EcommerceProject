from __future__ import absolute_import, unicode_literals
import os
import django
import time
from celery import Celery
from django.db import connections
from django.db.utils import OperationalError

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")

# Initialize Django
django.setup()

# Database connection check with retry logic
def db_connection_retry():
    db_conn = connections['default']
    max_retries = 5
    for _ in range(max_retries):
        try:
            db_conn.ensure_connection()
            return
        except OperationalError:
            time.sleep(2)  # Wait before retrying

db_connection_retry()  # Ensure database is available

# Initialize Celery
app = Celery("ecommerce")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
