from cms.models.pluginmodel import CMSPlugin
from django.db import models
from django.dispatch import receiver
import logging
from .utils import get_publications
from math import ceil

logger = logging.getLogger(__name__)
from pyzotero import zotero


from django.db.models.signals import post_save


# Create your models here.
class ZoteroPublications(CMSPlugin):
    api_key = models.CharField(max_length=200, default="")
    library_type = models.CharField(max_length=200, default="")
    library_id = models.CharField(max_length=200, default="")
    collection_id = models.CharField(max_length=200, default="", blank=True)
    style = models.CharField(max_length=200, default="apa")
    publications = models.JSONField(editable=False, default=dict)


# @receiver(post_save, sender=ZoteroPublications)
# def create_publications(sender, instance, *args, **kwargs):
#     logger.warning("create_publications ")
#     LIMIT = 10
#     startIndex = 0
#     publications = {}
#     params = {
#         "include": "bib,data",
#         "style": "apa",
#         "sort": "date",
#         "direction": "desc",
#         "linkwrap": 1,
#     }

#     zot = zotero.Zotero(
#         instance.get("library_id"),
#         instance.get("library_type"),
#         instance.get("api_key"),
#     )
#     if instance.get("collection_id"):
#         number_items = zot.num_collectionitems(instance.get("collection_id"))
#     else:
#         number_items = zot.count_items()
#         # add to request the items
#         params["start"] = startIndex
#         params["limit"] = LIMIT

#         for i in range(ceil(number_items / LIMIT)):
#             publications = get_publications(instance, params)
#             params["start"] = startIndex
#             startIndex += LIMIT

#         instance.publications = publications
