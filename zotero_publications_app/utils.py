from pyzotero import zotero
import logging
from .models import ZoteroPublications

logger = logging.getLogger(__name__)


def get_local_publciations_count(instanceId):
    local_instance = ZoteroPublications.objects.get(id=instanceId)
    count = 0
    for key, value in local_instance.publications.items():
        count += len(value)
    return count


def get_merged_publications_count(publications):
    count = 0
    for key, value in publications.items():
        count += len(value)
    return count


def get_remote_latest_version(instance):
    zot = zotero.Zotero(
        instance.get("library_id"),
        instance.get("library_type"),
        instance.get("api_key"),
    )

    latest_version = zot.last_modified_version()
    return latest_version


def get_publications(instance, params):
    try:
        # Initialize a dictionary to store publications by year
        publications_by_year = {}
        zot = zotero.Zotero(
            instance.get("library_id"),
            instance.get("library_type"),
            instance.get("api_key"),
        )
        if instance.get("collection_id"):
            items = zot.collection_items(instance.get("collection_id"), **params)
        else:

            # logging.warning(number_items)
            items = zot.items(**params)

            # Iterate through the data and populate the dictionary
            for item in items:
                # Extract the year from "parsedDate" (if available)
                parsed_date = item.get("meta", {}).get("parsedDate", "")
                year = parsed_date.split("-")[0] if parsed_date else "1300"
                # logging.warning(year)

                # Add the publication to the corresponding year's list
                if year not in publications_by_year:
                    publications_by_year[year] = []
                publications_by_year[year].append({item["key"]: item["bib"]})

    except Exception as e:
        publications_by_year = {"Error": [f"The following error: {e}"]}

    return publications_by_year


def get_trashed_publications_ids(instance, params):
    zot = zotero.Zotero(
        instance.get("library_id"),
        instance.get("library_type"),
        instance.get("api_key"),
    )

    # params = {
    #     "sort": "dateAdded",  # get the latest added
    #     "direction": "desc",  # get in asc order, so we can compare the latest added and indexes
    #     "linkwrap": 1,
    #     "start": 0,
    #     "limit": 100,
    # }

    trashed_items_ids = []
    items_trashed = zot.trash(**params)

    for item in items_trashed:
        # logging.warning(item)
        trashed_items_ids.append(item.get("key", ""))
    return trashed_items_ids


def get_deleted_publications_ids(instance):
    # Initialize a dictionary to store publications by year
    zot = zotero.Zotero(
        instance.get("library_id"),
        instance.get("library_type"),
        instance.get("api_key"),
    )
    params = {
        "since": instance.get("current_local_version"),
    }

    deleted_items_ids = []

    deleted_items_ids = zot.deleted(**params).get("items")
    # logger.warning(deleted_items_ids)

    # for item in deleted_items:
    #     deleted_items_ids.append(item.get("key", ""))

    return deleted_items_ids


def get_all_the_removed_publications_ids(instance, params):
    trashed_items_ids = get_trashed_publications_ids(instance, params)
    logger.warning(f"trashed {trashed_items_ids}")

    deleted_items_ids = get_deleted_publications_ids(instance)
    logger.warning(f"deleted {deleted_items_ids}")

    return trashed_items_ids + deleted_items_ids


def delete_publications_from_local_instance_by_id_list(instanceId, id_list):

    local_instance = ZoteroPublications.objects.get(id=instanceId)
    # for key, value in local_instance.publications.items():
    #     local_instance.publications[key] = [
    #         item for item in value if item.get("key", "") not in id_list
    #     ]

    for key, list_of_dicts in local_instance.publications.items():
        # Filter out dictionaries whose keys are in the ids_to_delete list
        local_instance.publications[key] = [
            d for d in list_of_dicts if list(d.keys())[0] not in id_list
        ]

    local_instance.save(update_fields=["publications"])

    return local_instance.publications


def merge_dicts_with_unique_values(dict1, dict2):
    """
    Merge two dictionaries with list of strings as values, ensuring that the values
    in the list for each key are unique.
    """
    sum = 0

    # Initialize the result dictionary
    result = {}

    # Combine all keys from both dictionaries
    all_keys = set(dict1) | set(dict2)

    logger.warning(dict1.keys())
    for key in all_keys:
        # Use set to automatically remove duplicates and union to merge
        unique_values = set(dict1.get(key, [])) | set(dict2.get(key, []))
        # unique_values = dict1.get(key, []) + dict2.get(key, [])

        # logger.warning(key)
        # logger.warning(len(unique_values))

        # Convert the set back to a list for the result
        result[key] = list(unique_values)

        sum += len(unique_values)

    logger.warning(sum)
    return result


def merge_dicts_allow_duplicates(dict1, dict2):
    """
    Merge two dictionaries where each key maps to a list of dictionaries with unique IDs as keys
    and HTML strings as values. The output is a dictionary with each key mapping to a list of HTML strings,
    allowing repeated values and preserving their order.
    """
    # Combine keys from both dictionaries
    all_keys = set(dict1.keys()) | set(dict2.keys())
    result = {}

    for key in all_keys:
        # Initialize a list for the current key to store HTML strings
        combined_list = []

        # Helper function to append HTML strings to the list
        def append_html_strings_to_list(dict_list):
            for dict_item in dict_list:
                for html_string in dict_item.values():
                    combined_list.append(html_string)

        # If the key is present in dict1, append its HTML strings to the list
        if key in dict1:
            append_html_strings_to_list(dict1[key])

        # If the key is present in dict2, also append its HTML strings to the list
        if key in dict2:
            append_html_strings_to_list(dict2[key])

        # Assign the combined list of HTML strings to the result
        result[key] = combined_list

    return result


def merge_dict_lists(dict1, dict2):
    """
    Merge two dictionaries containing lists of dictionaries, ensuring that dictionaries
    within the lists are not duplicated based on their keys.
    """
    # Initialize the result dictionary
    result = {}

    # Combine all keys from both dictionaries
    all_keys = set(dict1.keys()) | set(dict2.keys())

    for key in all_keys:
        # Initialize an empty list for the merged items under this key
        merged_items = []
        # Initialize a set to track which keys have been added to the merged list
        added_keys = set()

        # Function to append items if their key hasn't been added to the merged list
        def append_unique_items(item_list):
            for item in item_list:
                for item_key in item:
                    if item_key not in added_keys:
                        added_keys.add(item_key)
                        merged_items.append(item)

        # Append items from both dictionaries
        append_unique_items(dict1.get(key, []))
        append_unique_items(dict2.get(key, []))

        # Assign the merged items to the result dictionary
        result[key] = merged_items

    return result


def simplify_dict(input_dict):
    """
    Simplify the dictionary structure from a list of dictionaries with unique IDs
    as keys and HTML strings as values to a dictionary with each key mapping to a list
    of HTML strings.
    """
    simplified_dict = {}

    for key, list_of_dicts in input_dict.items():
        # Initialize a list to hold HTML strings for the current key
        html_strings = []

        # Extract HTML strings from each dictionary in the list and append them
        for dict_item in list_of_dicts:
            for html_string in dict_item.values():
                html_strings.append(html_string)

        # Assign the list of HTML strings to the current key in the simplified dictionary
        simplified_dict[key] = html_strings

    return simplified_dict
