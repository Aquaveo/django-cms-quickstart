from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from .models import HydroShareCommunityResourcesList

import logging

logger = logging.getLogger(__name__)


@plugin_pool.register_plugin
class HydroShareCommunityResourcesList(CMSPluginBase):
    model = HydroShareCommunityResourcesList
    name = _("HydroShare Community Resources Plugin")
    render_template = "hydroshare-community-resources.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context
