# Generated by Django 3.2 on 2023-12-05 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0027_alter_hydroshareresourcelist_resources'),
    ]

    operations = [
        migrations.AddField(
            model_name='hydroshareresourcelist',
            name='placeholder_image',
            field=models.CharField(default='https://picsum.photos/200', max_length=200),
        ),
    ]
