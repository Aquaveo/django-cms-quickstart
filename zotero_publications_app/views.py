from django.shortcuts import render
from django.http import JsonResponse
from pyzotero import zotero
import logging
import json
import math
from .models import ZoteroPublications
from .utils import (
    get_publications,
    get_local_publciations_count,
    merge_dict_lists,
    simplify_dict,
    get_all_the_removed_publications_ids,
    delete_publications_from_local_instance_by_id_list,
    get_remote_latest_version,
)

logger = logging.getLogger(__name__)


def base_view(request):

    context = {}
    return render(request, "zotero-publications-base.html", context)


# @timeit
def get_items_number(request):
    logging.warning("get_items_number")

    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)
    instance = {
        "library_id": body["library_id"],
        "library_type": body["library_type"],
        "api_key": body["api_key"],
        "collection_id": body["collection_id"],
    }
    # logging.warning(instance)

    zot = zotero.Zotero(
        instance.get("library_id"),
        instance.get("library_type"),
        instance.get("api_key"),
    )
    if instance.get("collection_id"):
        number_items = zot.num_collectionitems(instance.get("collection_id"))
    else:
        number_items = zot.count_items()

    instanceId = body["instanceID"]
    local_publications_count = get_local_publciations_count(instanceId)
    logging.warning(
        f"local publications count {local_publications_count} vs remote publications count {number_items}"
    )

    return JsonResponse({"number_items": number_items})


def initialize_publications_view(request):
    logging.warning("initialize_publications_view")
    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)
    instance = ZoteroPublications.objects.get(id=body["instanceID"])

    total_local_publications = body["totalLocalPublications"]
    total_remote_publications = body["totalRemotePublications"]

    difference_in_publications = total_remote_publications - total_local_publications
    LIMIT = 10
    START = 0
    iterations = math.ceil(difference_in_publications / LIMIT)

    new_local_instance_publications = instance.publications
    for i in range(iterations):
        logging.warning(f"getting publications {START+1} to {LIMIT+1}")
        params = {
            "include": "bib,data",
            "style": "apa",
            # "sort": "date",
            "sort": "dateAdded",  # get the latest added
            "direction": "asc",  # get in asc order, so we can compare the latest added and indexes
            "linkwrap": 1,
            "start": START,
            "limit": LIMIT,
        }
        publications_by_year = get_publications(instance, params)
        new_local_instance_publications = merge_dict_lists(
            new_local_instance_publications, publications_by_year
        )
        START += LIMIT

    instance.publications = new_local_instance_publications
    latest_version = get_remote_latest_version(instance)
    instance.local_remote_version = latest_version

    instance.save(update_fields=["publications", "local_remote_version"])

    publications = simplify_dict(new_local_instance_publications)

    return JsonResponse(publications)


def publications_view(request):
    # This dictionary can pass variables to the template.
    logging.warning("publications_view")

    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)

    instance_id = body["instanceID"]
    total_local_publications = body["totalLocalPublications"]
    total_remote_publications = body["totalRemotePublications"]

    instance = ZoteroPublications.objects.get(id=instance_id)
    # instance["current_local_version"] = instance.local_remote_version
    logging.warning(f"current version: {instance.local_remote_version}")

    latest_version = get_remote_latest_version(instance)
    logging.warning(f"latest version: {latest_version}")

    #  if no changes
    if total_local_publications == total_remote_publications:
        logging.warning("no changes, retrieving from database")
        new_local_instance_publications = instance.publications

    # adding or removing publications
    else:
        logging.warning(
            f"changes detected: {total_remote_publications - total_local_publications } publications"
        )
        get_trashed_items_params = {
            "style": "apa",
            "sort": "dateAdded",  # get the latest added
            "direction": "asc",  # get in asc order, so we can compare the latest added and indexes
            "linkwrap": 1,
            # "limit": 100,
            "since": instance.local_remote_version,
        }

        removed_publications_ids = get_all_the_removed_publications_ids(
            instance, get_trashed_items_params
        )
        logging.warning(f"removing publications: {removed_publications_ids}")

        new_local_instance_publications = (
            delete_publications_from_local_instance_by_id_list(
                instance, removed_publications_ids
            )
        )

        instance.publications = new_local_instance_publications
        params_add = {
            "include": "bib,data",
            "style": "apa",
            "sort": "dateAdded",  # get the latest added
            "direction": "asc",  # get in asc order, so we can compare the latest added and indexes
            "linkwrap": 1,
            "since": instance.local_remote_version,
        }
        logging.warning(f"adding publications")
        new_publications = get_publications(instance, params_add)
        new_local_instance_publications = merge_dict_lists(
            instance.publications, new_publications
        )
        instance.publications = new_local_instance_publications

    instance.local_remote_version = latest_version
    instance.save(update_fields=["publications", "local_remote_version"])
    publications = simplify_dict(new_local_instance_publications)
    return JsonResponse(publications)
