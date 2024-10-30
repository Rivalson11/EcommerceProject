from io import BytesIO

import pandas as pd
from celery import shared_task
from django.core.files.storage import default_storage
from django.db.models import Sum

from .models import Product, ProductCategories


@shared_task
def generate_stock_report():
    # Items needing restock
    products = Product.objects.filter(quantity__lt=5).values("product_id", "name", "quantity", "price")
    df = pd.DataFrame(products)
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)

    path = 'reports/stock_report.xlsx'
    with default_storage.open(path, 'wb') as f:
        f.write(output.read())

    return path


@shared_task
def generate_popularity_report():
    # Top 5 products by popularity score
    products = Product.objects.order_by('-popularity_score')[:5].values("product_id", "name", "popularity_score", "price")
    df = pd.DataFrame(products)
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)

    path = 'reports/popularity_report.xlsx'
    with default_storage.open(path, 'wb') as f:
        f.write(output.read())

    return path


@shared_task
def generate_category_report():
    # Category breakdown by popularity
    categories = ProductCategories.objects.annotate(
        total_popularity=Sum('product__popularity_score')
    )

    print(categories.values())

    df = pd.DataFrame(categories.values())
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)

    path = 'reports/category_report.xlsx'
    with default_storage.open(path, 'wb') as f:
        f.write(output.read())

    return path
