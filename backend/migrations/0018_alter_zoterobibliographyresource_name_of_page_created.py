# Generated by Django 3.2 on 2023-11-10 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0017_auto_20231109_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zoterobibliographyresource',
            name='name_of_page_created',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]