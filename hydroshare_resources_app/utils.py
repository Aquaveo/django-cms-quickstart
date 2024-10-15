import uuid
import requests
from bs4 import BeautifulSoup
import datetime

import logging

logger = logging.getLogger(__name__)


def get_dict_with_attribute(list_of_dicts, attribute, value):
    # Loop through each dictionary in the list
    for dictionary in list_of_dicts:
        # Check if the attribute exists in the dictionary and has the specified value
        if attribute in dictionary and dictionary[attribute] == value:
            return dictionary  # Return the dictionary if found

    return None  # Return None if not found in any dictionary


def get_most_recent_date(date_local_resource, date_api):
    # Convert strings to datetime objects
    date_time_local_resource = datetime.datetime.fromisoformat(date_local_resource[:-1])
    date_time_api = datetime.datetime.fromisoformat(date_api[:-1])
    # Compare the datetime objects
    if date_time_local_resource > date_time_api:
        return False
    elif date_time_local_resource < date_time_api:
        return True
    else:
        return False


def update_resource(resource, hs, instance):
    single_resource = {}
    if resource["resource_type"] == "ToolResource":
        science_metadata_json = hs.getScienceMetadata(resource["resource_id"])
        # logging.warning(f'{science_metadata_json}')
        image_url = science_metadata_json.get(
            "app_icon", instance.placeholder_image
        ).get("data_url", instance.placeholder_image)
        web_site_url = (
            ""
            if not science_metadata_json.get("app_home_page_url", "")
            else science_metadata_json.get("app_home_page_url").get("value", "")
        )
        github_url = (
            ""
            if not science_metadata_json.get("source_code_url", "")
            else science_metadata_json.get("source_code_url").get("value", "")
        )
        help_page_url = (
            ""
            if not science_metadata_json.get("help_page_url", "")
            else science_metadata_json.get("help_page_url").get("value", "")
        )
    if resource["resource_type"] == "CompositeResource":
        resource_scrapping = requests.get(resource["resource_url"])
        image_url = (
            instance.placeholder_image
            if not extract_value_by_name(resource_scrapping.content, "app_icon")
            else extract_value_by_name(resource_scrapping.content, "app_icon")
        )
        web_site_url = (
            ""
            if not extract_value_by_name(resource_scrapping.content, "home_page_url")
            else extract_value_by_name(resource_scrapping.content, "home_page_url")
        )
        github_url = (
            ""
            if not extract_value_by_name(resource_scrapping.content, "source_code_url")
            else extract_value_by_name(resource_scrapping.content, "source_code_url")
        )
        help_page_url = (
            ""
            if not extract_value_by_name(resource_scrapping.content, "help_page_url")
            else extract_value_by_name(resource_scrapping.content, "help_page_url")
        )

    if image_url == "":
        image_url = instance.placeholder_image

    single_resource = {
        "title": resource["resource_title"],
        "abstract": resource["abstract"],
        "github_url": github_url,
        "image": image_url,
        "web_site_url": web_site_url,
        "documentation_url": help_page_url,
        "resource_id": resource["resource_id"],
        "date_last_updated": resource["date_last_updated"],
        "resource_type": resource["resource_type"],
        "resource_url": resource["resource_url"],
    }
    return single_resource


def extract_value_by_name(html, name):
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("#extraMetaTable tbody tr")

    for row in rows:
        name_cell = row.select_one("td:first-child")
        value_cell = row.select_one("td:nth-child(2)")

        if name_cell and value_cell and name_cell.get_text(strip=True) == name:
            return value_cell.get_text(strip=True)

    return None
