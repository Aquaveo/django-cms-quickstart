from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from .models import (
    HydroLearnModulesList,
)

import logging

logger = logging.getLogger(__name__)


@plugin_pool.register_plugin
class HydroLearnModulesPlugin(CMSPluginBase):
    model = HydroLearnModulesList
    name = _("HydroLearn Modules Plugin")
    render_template = "hydrolearn-modules.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context
