# Generated by Django 4.2.4 on 2023-10-13 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0017_location_alter_profile_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='font_preference',
            field=models.CharField(default='Young Serif', max_length=50),
        ),
    ]
