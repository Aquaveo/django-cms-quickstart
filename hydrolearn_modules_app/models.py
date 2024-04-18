from cms.models.pluginmodel import CMSPlugin
from django.db import models
import logging

logger = logging.getLogger(__name__)


class HydroLearnModulesList(CMSPlugin):
    tag_filter = models.CharField(max_length=200, default="nwm_portal_module")
    placeholder_image = models.CharField(
        max_length=200, default="https://placehold.co/200"
    )
    modules = models.JSONField(editable=False, default=dict)
