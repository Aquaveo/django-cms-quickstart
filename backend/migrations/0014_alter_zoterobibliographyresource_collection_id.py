# Generated by Django 3.2 on 2023-11-02 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_alter_zoterobibliographyresource_collection_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zoterobibliographyresource',
            name='collection_id',
            field=models.CharField(default='collection_id', max_length=200, null=True),
        ),
    ]
