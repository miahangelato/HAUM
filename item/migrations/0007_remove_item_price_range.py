# Generated by Django 4.2.4 on 2023-10-14 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0006_pricerange_item_price_range'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='price_range',
        ),
    ]
