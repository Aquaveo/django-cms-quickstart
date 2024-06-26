# Generated by Django 3.2 on 2023-10-17 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_alter_hydroshareresource_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hydroshareresource',
            name='documentation_url',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='hydroshareresource',
            name='github_url',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='hydroshareresource',
            name='image',
            field=models.CharField(default='https://placehold.co/400', max_length=200),
        ),
        migrations.AlterField(
            model_name='hydroshareresource',
            name='subtitle',
            field=models.CharField(default='resource subtitle', max_length=200),
        ),
        migrations.AlterField(
            model_name='hydroshareresource',
            name='title',
            field=models.CharField(default='resource title', max_length=200),
        ),
        migrations.AlterField(
            model_name='hydroshareresource',
            name='web_site_url',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
