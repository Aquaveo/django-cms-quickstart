# Generated by Django 3.2 on 2023-11-10 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0020_alter_zoterobibliographyresource_name_of_page_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zoterobibliographyresource',
            name='name_of_page_created',
            field=models.CharField(blank=True, default='', max_length=200, unique=True),
        ),
    ]
