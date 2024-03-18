from django import template
from pyzotero import zotero
import logging
import time

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def loading_indicator(instance):
    # Assuming `instance` has a method or property to check if a field is being saved
    logger.warning(instance._state.adding)
    pubs = create_html_citations(instance)
    # is_saving = getattr(instance, f"{field_name}", False)

    # if is_saving:
    # Return HTML for the loading indicator
    return pubs
    # else:
    #     # Return an empty string or any other placeholder if not saving
    #     return ""


def create_html_citations(instance):
    logger.warning("creating_html_citations ")
    params = {
        "include": "bib,data",
        "style": "apa",
        "sort": "date",
        "direction": "desc",
        "linkwrap": 1,
    }
    try:
        time.sleep(5)
        zot = zotero.Zotero(
            instance.library_id, instance.library_type, instance.api_key
        )
        if instance.collection_id:
            items = zot.collection_items(instance.collection_id, **params)
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

        return publications_by_year
    except Exception as e:
        return publications_by_year

    # {% load static %}

    # {% load loading_tag %}

    # {% loading_indicator instance as pubs %}
    #     <div class="container-zotero-plugin">
    #         {% for key, values in pubs.items %}
    #         <div class="wrapper-publication-set">
    #             <h2 class="year-style">{{ key }}</h2>

    #                 {% for citation in values %}

    #                     {{ citation | safe }}

    #                 {% endfor %}

    #         </div>
    #         {% endfor %}
    #     </div>
