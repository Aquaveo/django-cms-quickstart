# Generated by Django 3.2 on 2023-11-09 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0016_auto_20231103_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='zoterobibliographyresource',
            name='name_of_page_created',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='zoterobibliographyresource',
            name='updated_version',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
