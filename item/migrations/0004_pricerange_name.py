# Generated by Django 4.2.4 on 2023-10-13 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0003_pricerange_item_price_range'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricerange',
            name='name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
