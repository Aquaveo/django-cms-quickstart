from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from .models import HydroShareResource

@plugin_pool.register_plugin
class HydroShareResourcePlugin(CMSPluginBase):
    model = HydroShareResource
    name = _("HydroShare Resource Plugin")
    render_template = "hydroshare_resource_template.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context