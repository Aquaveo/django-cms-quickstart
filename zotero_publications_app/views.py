from django.shortcuts import render
from django.http import JsonResponse
from pyzotero import zotero
import logging
import json

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
    instance = {
        "library_id": body["library_id"],
        "library_type": body["library_type"],
        "api_key": body["api_key"],
        "collection_id": body["collection_id"],
        "instanceId": body["instanceID"],
    }
    params = {
        "include": "bib,data",
        "style": "apa",
        # "sort": "date",
        "sort": "dateAdded",  # get the latest added
        "direction": "asc",  # get in asc order, so we can compare the latest added and indexes
        "linkwrap": 1,
        "start": body["start"],
        "limit": body["limit"],
    }
    instance_id = body["instanceID"]
    totalLocalPublications = body["totalLocalPublications"]
    totalRemotePublications = body["totalRemotePublications"]

    local_instance = ZoteroPublications.objects.get(id=instance_id)
    instance["current_local_version"] = local_instance.local_remote_version
    logging.warning(f"current version: {instance['current_local_version']}")

    latest_version = get_remote_latest_version(instance)
    logging.warning(f"latest version: {latest_version}")

    publications_by_year = get_publications(instance, params)

    new_local_instance_publications = merge_dict_lists(
        local_instance.publications, publications_by_year
    )

    local_instance.publications = new_local_instance_publications
    local_instance.local_remote_version = latest_version
    local_instance.save(update_fields=["publications", "local_remote_version"])
    publications = simplify_dict(new_local_instance_publications)
    return JsonResponse(publications)


def publications_view(request):
    # This dictionary can pass variables to the template.
    logging.warning("publications_view")

    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)
    instance = {
        "library_id": body["library_id"],
        "library_type": body["library_type"],
        "api_key": body["api_key"],
        "collection_id": body["collection_id"],
        "instanceId": body["instanceID"],
    }
    params = {
        "include": "bib,data",
        "style": "apa",
        # "sort": "date",
        "sort": "dateAdded",  # get the latest added
        "direction": "asc",  # get in asc order, so we can compare the latest added and indexes
        "linkwrap": 1,
        "start": body["start"],
        "limit": body["limit"],
    }
    instance_id = body["instanceID"]
    totalLocalPublications = body["totalLocalPublications"]
    totalRemotePublications = body["totalRemotePublications"]

    local_instance = ZoteroPublications.objects.get(id=instance_id)
    instance["current_local_version"] = local_instance.local_remote_version
    logging.warning(f"current version: {instance['current_local_version']}")

    latest_version = get_remote_latest_version(instance)
    logging.warning(f"latest version: {latest_version}")

    # logging.warning(local_instance)
    # if added new publications remotely
    # if totalRemotePublications > totalLocalPublications:
    #     logging.warning("adding publications")
    #     publications_by_year = get_publications(instance, params)
    #     # for key, value in publications_by_year.items():
    #     #     for item in value:
    #     #         logging.warning(f"{item.keys()}")

    #     # logging.warning("local publications")

    #     # for key, value in local_instance.publications.items():
    #     #     for item in value:
    #     #         logging.warning(f"{item.keys()}")

    #     # local_publications_count = get_local_publciations_count(instance_id)
    #     # logging.warning(local_publications_count)

    #     new_local_instance_publications = merge_dict_lists(
    #         local_instance.publications, publications_by_year
    #     )
    #     # new_local_instance_publications_count = get_merged_publications_count(
    #     #     new_local_instance_publications
    #     # )
    #     # publications_by_year_count = get_merged_publications_count(publications_by_year)

    #     # logging.warning(
    #     #     f"{new_local_instance_publications_count} {publications_by_year_count}"
    #     # )

    #     local_instance.publications = new_local_instance_publications

    # #  if deleted publications remotely
    # if totalRemotePublications < totalLocalPublications:
    #     logging.warning("removing publications")
    #     get_trashed_items_params = {
    #         "style": "apa",
    #         "sort": "dateAdded",  # get the latest added
    #         "direction": "asc",  # get in asc order, so we can compare the latest added and indexes
    #         "linkwrap": 1,
    #         "limit": body["limit"],
    #         "since": local_instance.local_remote_version,
    #     }

    #     removed_publications_ids = get_all_the_removed_publications_ids(
    #         instance, get_trashed_items_params
    #     )
    #     logging.warning(f"removing publications: {removed_publications_ids}")

    #     logging.warning(f"before_publications")

    #     for key, value in local_instance.publications.items():
    #         for item in value:
    #             logging.warning(f"{item.keys()}")

    #     new_local_instance_publications = (
    #         delete_publications_from_local_instance_by_id_list(
    #             instance_id, removed_publications_ids
    #         )
    #     )
    #     logging.warning(f"final publications:")

    #     for key, value in new_local_instance_publications.items():
    #         for item in value:
    #             logging.warning(f"{item.keys()}")

    #     local_instance.publications = new_local_instance_publications

    #  if no changes
    if totalRemotePublications == totalLocalPublications:
        logging.warning("no changes")
        new_local_instance_publications = local_instance.publications

    # adding or removing publications
    if local_instance.local_remote_version != 0:

        # logging.warning("removing publications")
        get_trashed_items_params = {
            "style": "apa",
            "sort": "dateAdded",  # get the latest added
            "direction": "asc",  # get in asc order, so we can compare the latest added and indexes
            "linkwrap": 1,
            "limit": body["limit"],
            "since": local_instance.local_remote_version,
        }

        removed_publications_ids = get_all_the_removed_publications_ids(
            instance, get_trashed_items_params
        )
        logging.warning(f"removing publications: {removed_publications_ids}")

        # logging.warning(f"before_publications")

        # for key, value in local_instance.publications.items():
        #     for item in value:
        #         logging.warning(f"{item.keys()}")

        new_local_instance_publications = (
            delete_publications_from_local_instance_by_id_list(
                instance_id, removed_publications_ids
            )
        )
        # logging.warning(f"final publications:")

        # for key, value in new_local_instance_publications.items():
        #     for item in value:
        #         logging.warning(f"{item.keys()}")

        local_instance.publications = new_local_instance_publications
        params_add = {
            "include": "bib,data",
            "style": "apa",
            "sort": "dateAdded",  # get the latest added
            "direction": "asc",  # get in asc order, so we can compare the latest added and indexes
            "linkwrap": 1,
            "since": local_instance.local_remote_version,
        }
        logging.warning(f"adding publications")
        new_publications = get_publications(instance, params_add)
        new_local_instance_publications = merge_dict_lists(
            local_instance.publications, new_publications
        )
        local_instance.publications = new_local_instance_publications

    # else:
    #     publications_by_year = get_publications(instance, params)
    #     new_local_instance_publications = merge_dict_lists(
    #         local_instance.publications, publications_by_year
    #     )

    #     local_instance.publications = new_local_instance_publications
    #     local_instance.save(update_fields=["publications"])

    # if is_remote:
    #     publications_by_year = get_publications(instance, params)
    #     logging.warning("remote instance")
    #     sum = 0

    #     logging.warning(publications_by_year.keys())
    #     logging.warning(local_instance.publications.keys())

    #     new_local_instance_publications = merge_dict_lists(
    #         local_instance.publications, publications_by_year
    #     )
    #     sum = 0

    #     for key, value in new_local_instance_publications.items():
    #         logging.warning(f"{key}: {len(value)}")
    #         sum += len(value)
    #     logging.warning(f"sum: {sum}")

    #     local_instance.publications = new_local_instance_publications
    #     local_instance.save(update_fields=["publications"])
    # else:
    #     publications_by_year = local_instance.publications

    # first edit
    # try:
    #     # Initialize a dictionary to store publications by year
    #     publications_by_year = {}
    #     zot = zotero.Zotero(
    #         instance.get("library_id"),
    #         instance.get("library_type"),
    #         instance.get("api_key"),
    #     )
    #     if instance.get("collection_id"):
    #         items = zot.collection_items(instance.get("collection_id"), **params)
    #     else:

    #         # logging.warning(number_items)
    #         items = zot.items(**params)

    #         # Iterate through the data and populate the dictionary
    #         for item in items:
    #             # Extract the year from "parsedDate" (if available)
    #             parsed_date = item.get("meta", {}).get("parsedDate", "")
    #             year = parsed_date.split("-")[0] if parsed_date else "1300"
    #             # logging.warning(year)

    #             # Add the publication to the corresponding year's list
    #             if year not in publications_by_year:
    #                 publications_by_year[year] = []
    #             publications_by_year[year].append(item["bib"])

    # except Exception as e:
    #     publications_by_year = {"Error": [f"The following error: {e}"]}

    local_instance.local_remote_version = latest_version
    local_instance.save(update_fields=["publications", "local_remote_version"])
    publications = simplify_dict(new_local_instance_publications)
    return JsonResponse(publications)
