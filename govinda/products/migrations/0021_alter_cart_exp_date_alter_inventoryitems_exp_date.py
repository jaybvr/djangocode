# Generated by Django 4.1.1 on 2023-10-23 03:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_orders_gift'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='exp_date',
            field=models.DateField(default=datetime.date(9999, 11, 11)),
        ),
        migrations.AlterField(
            model_name='inventoryitems',
            name='exp_date',
            field=models.DateField(default=datetime.date(9999, 11, 11)),
        ),
    ]
