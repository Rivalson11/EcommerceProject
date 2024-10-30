import os

import pandas as pd
from celery import shared_task
from django.conf import settings
from django.db.models import Sum

from .models import Product, ProductCategories


@shared_task
def generate_stock_report():
    # Items needing restock
    products = Product.objects.filter(quantity__lt=5).values("product_id", "name", "quantity", "price")
    df = pd.DataFrame(products)

    # Set the path relative to MEDIA_ROOT
    relative_path = 'reports/stock_report.xlsx'
    report_path = os.path.join(settings.MEDIA_ROOT, relative_path)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    # Save the DataFrame directly to an Excel file
    df.to_excel(report_path, index=False, engine='openpyxl')

    # Return the relative path for storage in the TaskResult
    return relative_path


@shared_task
def generate_popularity_report():
    # Top 5 products by popularity score
    products = Product.objects.order_by("-popularity_score")[:5].values(
        "product_id", "name", "popularity_score", "price"
    )
    df = pd.DataFrame(products)
    # Set the path relative to MEDIA_ROOT
    relative_path = 'reports/stock_report.xlsx'
    report_path = os.path.join(settings.MEDIA_ROOT, relative_path)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    # Save the DataFrame directly to an Excel file
    df.to_excel(report_path, index=False, engine='openpyxl')

    # Return the relative path for storage in the TaskResult
    return relative_path


@shared_task
def generate_category_report():
    # Category breakdown by popularity
    categories = ProductCategories.objects.annotate(total_popularity=Sum("product__popularity_score"))

    df = pd.DataFrame(categories.values())
    # Set the path relative to MEDIA_ROOT
    relative_path = 'reports/stock_report.xlsx'
    report_path = os.path.join(settings.MEDIA_ROOT, relative_path)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    # Save the DataFrame directly to an Excel file
    df.to_excel(report_path, index=False, engine='openpyxl')

    # Return the relative path for storage in the TaskResult
    return relative_path
