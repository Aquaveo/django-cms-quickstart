from pyzotero import zotero


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
                publications_by_year[year].append(item["bib"])

    except Exception as e:
        publications_by_year = {"Error": [f"The following error: {e}"]}

    return publications_by_year


def merge_dict_lists(dict1, dict2):
    """
    Merge two dictionaries that have lists as values. If there are overlapping
    keys, merge their lists without repeating elements.

    Parameters:
    - dict1: The first dictionary.
    - dict2: The second dictionary.

    Returns:
    - A new dictionary with merged keys and lists.
    """
    # Initialize the result dictionary
    merged_dict = {}

    # Combine the keys from both dictionaries
    all_keys = set(dict1) | set(dict2)

    for key in all_keys:
        # If the key is in both dictionaries, merge the lists without duplicates
        if key in dict1 and key in dict2:
            merged_dict[key] = list(set(dict1[key] + dict2[key]))
        # If the key is only in one of the dictionaries, just add it to the result
        elif key in dict1:
            merged_dict[key] = dict1[key]
        else:
            merged_dict[key] = dict2[key]

    return merged_dict
