# Generated by Django 3.2 on 2023-11-01 19:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_auto_20231101_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hydroshareresource',
            name='height',
            field=models.PositiveIntegerField(default=200, validators=[django.core.validators.MinValueValidator(150), django.core.validators.MaxValueValidator(400)]),
        ),
        migrations.AlterField(
            model_name='hydroshareresource',
            name='image',
            field=models.CharField(default='https://picsum.photos/200', max_length=200),
        ),
        migrations.AlterField(
            model_name='hydroshareresource',
            name='width',
            field=models.PositiveIntegerField(default=200, validators=[django.core.validators.MinValueValidator(150), django.core.validators.MaxValueValidator(400)]),
        ),
    ]