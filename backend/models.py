from cms.models.pluginmodel import CMSPlugin

from django.db import models
import uuid

class HydroShareResource(CMSPlugin):
    title = models.CharField(max_length=200, default='resource title')
    subtitle = models.CharField(max_length=200, default='resource subtitle')
    image = models.CharField(max_length=200, default='https://placehold.co/400')
    description= models.TextField(default='resource description')
    github_url=models.CharField(max_length=200, default='', blank=True)
    documentation_url=models.CharField(max_length=200, default='', blank=True)
    web_site_url=models.CharField(max_length=200, default='', blank=True)
    unique_identifier=models.UUIDField(default=uuid.uuid4, editable=False)