from cms.models.pluginmodel import CMSPlugin
from django.db import models
import logging

logger = logging.getLogger(__name__)


class HydroShareCommunityResourcesList(CMSPlugin):
    user = models.CharField(max_length=200, default="", blank=True)
    password = models.CharField(max_length=200, default="", blank=True)
    community_id = models.CharField(max_length=200, default="")
    placeholder_image = models.CharField(
        max_length=200, default="https://www.tethysplatform.org/images/tethys_data.png"
    )
    updated_version = models.IntegerField(default=0, editable=False)
    resources = models.JSONField(editable=False, default=dict)
