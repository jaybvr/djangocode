# Generated by Django 4.1.1 on 2023-06-02 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_inventoryitems_exp_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='igst',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='inventoryitems',
            name='igst',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='itemsales',
            name='igst',
            field=models.FloatField(default=0),
        ),
    ]
