from django.shortcuts import render
from django.http import JsonResponse
from pyzotero import zotero
import logging
import json

from .models import ZoteroPublications
from .utils import (
    get_publications,
    merge_dicts_with_unique_values,
    merge_dicts_allow_duplicates,
    merge_dict_lists,
    simplify_dict,
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
    logging.warning(instance)

    zot = zotero.Zotero(
        instance.get("library_id"),
        instance.get("library_type"),
        instance.get("api_key"),
    )
    if instance.get("collection_id"):
        number_items = zot.num_collectionitems(instance.get("collection_id"))
    else:
        number_items = zot.count_items()

    return JsonResponse({"number_items": number_items})


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
    # is_remote = body["isRemote"]

    local_instance = ZoteroPublications.objects.get(id=instance_id)
    # logging.warning(local_instance)
    #  if added new publications remotely
    if totalRemotePublications > totalLocalPublications:
        logging.warning("adding publications")
        publications_by_year = get_publications(instance, params)

        new_local_instance_publications = merge_dict_lists(
            local_instance.publications, publications_by_year
        )

        local_instance.publications = new_local_instance_publications
        local_instance.save(update_fields=["publications"])

    #  if deleted publications remotely
    if totalRemotePublications < totalLocalPublications:
        logging.warning("removing publications")

        new_local_instance_publications = get_publications(instance, params)
        logging.warning(new_local_instance_publications)

        local_instance.publications = new_local_instance_publications
        local_instance.save(update_fields=["publications"])

    #  if no changes
    else:
        logging.warning("no changes")

        new_local_instance_publications = local_instance.publications

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
    publications = simplify_dict(new_local_instance_publications)
    return JsonResponse(publications)
