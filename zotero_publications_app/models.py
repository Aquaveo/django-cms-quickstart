from cms.models.pluginmodel import CMSPlugin
from django.db import models
import logging

logger = logging.getLogger(__name__)


# Create your models here.
class ZoteroPublications(CMSPlugin):
    api_key = models.CharField(max_length=200, default="")
    library_type = models.CharField(max_length=200, default="")
    library_id = models.CharField(max_length=200, default="")
    collection_id = models.CharField(max_length=200, default="", blank=True)
    style = models.CharField(max_length=200, default="apa")
    publications = models.JSONField(editable=False, default=dict)
