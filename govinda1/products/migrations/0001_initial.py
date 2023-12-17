# Generated by Django 4.2.7 on 2023-12-03 15:35

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessUnit',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=1000)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('item_code', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
                ('unit', models.CharField(default='', max_length=100)),
                ('order_quantity', models.IntegerField(default=0)),
                ('item_price', models.FloatField(default=0)),
                ('igst', models.FloatField(default=0)),
                ('cgst', models.FloatField(default=0)),
                ('sgst', models.FloatField(default=0)),
                ('tax', models.FloatField(default=0)),
                ('item_net_price', models.FloatField(default=0)),
                ('order_price', models.FloatField(default=0)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('exp_date', models.DateField(default=datetime.date(9999, 11, 11))),
                ('damage', models.BooleanField(default=False)),
                ('item_group', models.CharField(max_length=500)),
                ('bu', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('customer_mobile', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=500)),
                ('customer_mailid', models.EmailField(max_length=254)),
                ('customer_address', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='InventoryGroups',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=1000)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('bu', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.businessunit')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('order_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('order_status', models.CharField(max_length=20)),
                ('order_date', models.DateTimeField()),
                ('item_price', models.FloatField(default=0)),
                ('tax', models.FloatField(default=0)),
                ('order_total', models.FloatField(default=0)),
                ('cash', models.FloatField(default=0)),
                ('online', models.FloatField(default=0)),
                ('transaction_id', models.CharField(default='XXXX', max_length=100)),
                ('gift', models.BooleanField(default=False)),
                ('damage', models.BooleanField(default=False)),
                ('customer_mobile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.customers')),
            ],
        ),
        migrations.CreateModel(
            name='ItemSales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_code', models.CharField(max_length=200)),
                ('item_name', models.CharField(max_length=500)),
                ('unit', models.CharField(default='', max_length=100)),
                ('bu', models.CharField(max_length=200)),
                ('group', models.CharField(max_length=200)),
                ('order_quantity', models.IntegerField(default=0)),
                ('item_price', models.FloatField(default=0)),
                ('igst', models.FloatField(default=0)),
                ('cgst', models.FloatField(default=0)),
                ('sgst', models.FloatField(default=0)),
                ('tax', models.FloatField(default=0)),
                ('item_net_price', models.FloatField(default=0)),
                ('order_price', models.FloatField(default=0)),
                ('damage', models.BooleanField(default=False)),
                ('customer_mobile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.customers')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.orders')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryItems',
            fields=[
                ('item_code', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
                ('unit', models.CharField(default='', max_length=100)),
                ('available_quantity', models.IntegerField(default=0)),
                ('price', models.FloatField(default=0)),
                ('igst', models.FloatField(default=0)),
                ('cgst', models.FloatField(default=0)),
                ('sgst', models.FloatField(default=0)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('exp_date', models.DateField(default=datetime.date(9999, 11, 11))),
                ('damage', models.BooleanField(default=False)),
                ('bu', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.businessunit')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.inventorygroups')),
            ],
        ),
    ]