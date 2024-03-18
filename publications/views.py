from django.shortcuts import render
from django.http import JsonResponse
from pyzotero import zotero
from .models import ZoteroPublications
import logging
import json

logger = logging.getLogger(__name__)


def base_view(request):
    # This dictionary can pass variables to the template.
    logging.warning("base_view")
    context = {}
    return render(request, "publications/base.html", context)


def publications_view(request):
    # This dictionary can pass variables to the template.
    logging.warning("publications_view")

    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)
    logging.warning(body["library_id"])
    instance = {
        "library_id": body["library_id"],
        "library_type": body["library_type"],
        "api_key": body["api_key"],
        "collection_id": body["collection_id"],
    }
    params = {
        "include": "bib,data",
        "style": "apa",
        "sort": "date",
        "direction": "desc",
        "linkwrap": 1,
    }

    try:
        zot = zotero.Zotero(
            instance.get("library_id"),
            instance.get("library_type"),
            instance.get("api_key"),
        )
        if instance.get("collection_id"):
            items = zot.collection_items(instance.get("collection_id"), **params)
        else:
            items = zot.items(**params)
        # Initialize a dictionary to store publications by year
        publications_by_year = {}

        # Iterate through the data and populate the dictionary
        for item in items:
            # Extract the year from "parsedDate" (if available)
            parsed_date = item.get("meta", {}).get("parsedDate", "")
            year = parsed_date.split("-")[0] if parsed_date else "More Publications"

            # Add the publication to the corresponding year's list
            if year not in publications_by_year:
                publications_by_year[year] = []
            publications_by_year[year].append(item["bib"])

        publications_by_year

    except Exception as e:
        publications_by_year = {"Error": [f"The following error: {e}"]}

    return JsonResponse(publications_by_year)
