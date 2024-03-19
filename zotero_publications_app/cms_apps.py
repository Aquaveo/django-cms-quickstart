from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


@apphook_pool.register  # register the application
class ZoteroPublicationsAppApphook(CMSApp):
    app_name = "zotero_publications_app"
    name = "Zotero Publications Application"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["zotero_publications_app.urls"]
