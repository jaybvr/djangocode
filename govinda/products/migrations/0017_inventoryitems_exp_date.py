# Generated by Django 4.1.1 on 2023-04-15 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_businessunit_cart_bu_itemsales_bu_inventorygroups_bu_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitems',
            name='exp_date',
            field=models.DateField(default=None),
        ),
    ]