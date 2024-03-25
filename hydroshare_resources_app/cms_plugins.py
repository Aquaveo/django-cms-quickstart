from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from .models import HydroShareResourcesList

import logging

logger = logging.getLogger(__name__)


@plugin_pool.register_plugin
class HydroShareResourcesList(CMSPluginBase):
    model = HydroShareResourcesList
    name = _("HydroShare Resources Plugin")
    render_template = "hydroshare-resources.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context
