from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from .models import ZoteroPublications


import logging

logger = logging.getLogger(__name__)


@plugin_pool.register_plugin
class ZoteroPlugin(CMSPluginBase):
    model = ZoteroPublications
    name = _("Zotero Publications Plugin")
    render_template = "zotero-publications.html"
    cache = False

    # This is key in order to call the API every time the page renders
    # The instance.save calls the pre_save signal which makes the call of the API
    def render(self, context, instance, placeholder):
        logging.warning("init rendering zotero plugin")
        context = super().render(context, instance, placeholder)
        logging.warning("finish rendering zotero plugin")
        return context
