# Generated by Django 3.2 on 2023-10-04 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20231004_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hydroshareresource',
            name='documentation_url',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='hydroshareresource',
            name='github_url',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='hydroshareresource',
            name='web_site_url',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]