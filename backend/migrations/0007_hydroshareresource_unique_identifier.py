# Generated by Django 3.2 on 2023-10-09 16:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20231004_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='hydroshareresource',
            name='unique_identifier',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
