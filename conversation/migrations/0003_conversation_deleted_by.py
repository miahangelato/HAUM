# Generated by Django 4.2.4 on 2023-10-27 16:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conversation', '0002_remove_conversationmessage_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='deleted_by',
            field=models.ManyToManyField(related_name='deleted_conversations', to=settings.AUTH_USER_MODEL),
        ),
    ]
