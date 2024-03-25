from cms.models.pluginmodel import CMSPlugin
from django.db import models


import logging

logger = logging.getLogger(__name__)


class HydroShareResourceList(CMSPlugin):
    user = models.CharField(max_length=200, default="", blank=True)
    password = models.CharField(max_length=200, default="", blank=True)
    placeholder_image = models.CharField(
        max_length=200, default="https://picsum.photos/200"
    )
    tags = models.CharField(max_length=200, default="")
    updated_version = models.IntegerField(default=0, editable=False)
    resources = models.JSONField(editable=False, default=dict)
