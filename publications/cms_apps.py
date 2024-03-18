from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


@apphook_pool.register  # register the application
class PublicationsApphook(CMSApp):
    app_name = "publications"
    name = "Zotero Publications Application"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["publications.urls"]
