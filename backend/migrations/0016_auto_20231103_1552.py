# Generated by Django 3.2 on 2023-11-03 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0015_alter_zoterobibliographyresource_collection_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zoterobibliographyresource',
            name='api_key',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='zoterobibliographyresource',
            name='collection_id',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='zoterobibliographyresource',
            name='library_id',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='zoterobibliographyresource',
            name='library_type',
            field=models.CharField(default='', max_length=200),
        ),
    ]
