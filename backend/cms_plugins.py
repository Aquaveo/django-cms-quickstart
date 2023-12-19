from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from .models import HydroShareResource,HydroShareResourceList,ZoteroBibliographyResource
import logging


logger = logging.getLogger(__name__)

@plugin_pool.register_plugin
class HydroShareResourcePlugin(CMSPluginBase):
    model = HydroShareResource
    name = _("HydroShare Resource Plugin")
    render_template = "hydroshare_resource_template.html"
    cache = False
    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class HydroShareResourceListPlugin(CMSPluginBase):
    model = HydroShareResourceList
    name = _("HydroShare Resource List Plugin")
    render_template = "hydroshare_list_resources.html"
    cache = False
    def render(self, context, instance, placeholder):
        instance.updated_version = instance.updated_version + 1
        instance.save(update_fields=['updated_version'])
        context = super().render(context, instance, placeholder)
        return context

@plugin_pool.register_plugin
class ZoteroBibliographyResourcePlugin(CMSPluginBase):
    model = ZoteroBibliographyResource
    name = _("Zotero Citation Resource Plugin")
    render_template = "zotero_bibliography.html"
    cache = False

    #This is key in order to call the API every time the page renders
    #The instance.save calls the pre_save signal which makes the call of the API
    def render(self, context, instance, placeholder):
        instance.updated_version = instance.updated_version + 1
        instance.save(update_fields=['updated_version'])
        context = super().render(context, instance, placeholder)
        return context
      