from cms.models.pluginmodel import CMSPlugin

from django.db import models

class HydroShareResource(CMSPlugin):
    title = models.CharField(max_length=50, default='resource title')
    subtitle = models.CharField(max_length=50, default='resource subtitle')
    image = models.CharField(max_length=50, default='https://placehold.co/400')
    description= models.TextField(max_length=150, default='resource description')
    github_url=models.CharField(max_length=50, default='', blank=True)
    documentation_url=models.CharField(max_length=50, default='', blank=True)
    web_site_url=models.CharField(max_length=50, default='', blank=True)