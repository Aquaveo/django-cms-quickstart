# Generated by Django 3.2 on 2024-03-04 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('backend', '0028_hydroshareresourcelist_placeholder_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='HydroLearnModulesList',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='backend_hydrolearnmoduleslist', serialize=False, to='cms.cmsplugin')),
                ('organization', models.CharField(blank=True, default='', max_length=200)),
                ('placeholder_image', models.CharField(default='https://picsum.photos/200', max_length=200)),
                ('updated_version', models.IntegerField(default=0, editable=False)),
                ('modules', models.JSONField(default=dict, editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
