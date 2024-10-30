# Generated by Django 4.2.13 on 2024-10-29 17:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('purchasing', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PrePurchase',
            fields=[
                ('purchase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='purchasing.purchase')),
                ('shopping_cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchasing.shoppingcart')),
            ],
            bases=('purchasing.purchase',),
        ),
    ]