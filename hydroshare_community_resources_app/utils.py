import requests
from bs4 import BeautifulSoup
import json
from itertools import chain
import datetime
import re


def get_curated_resources(
    composite_resource_id="302dcbef13614ac486fb260eaa1ca87c", hs=None
):
    science = hs.getScienceMetadata(composite_resource_id)
    relations = science.get("relations", [])
    resource_ids = []
    for item in relations:
        if item.get("type") == "hasPart":
            value = item.get("value", "")
            # Regular expression to find the resource ID in the URL
            match = re.search(
                r"http://www\.hydroshare\.org/resource/([a-f0-9]{32})", value
            )
            if match:
                resource_id = match.group(1)
                resource_ids.append(resource_id)
    return resource_ids


def filter_resources_list_by_resources_id(resources, ids):
    filtered_resources = []
    for resource in resources:
        if resource["resource_id"] in ids:
            filtered_resources.append(resource)
    return filtered_resources


def join_generators(generators):
    seen_resource_ids = set()
    for gen in generators:
        for item in gen:
            resource_id = item.get("resource_id")
            if resource_id not in seen_resource_ids:
                seen_resource_ids.add(resource_id)
                yield item


def get_group_ids(community_id):
    url = f"https://www.hydroshare.org/community/{community_id}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    group_ids = []

    # Find the script tag with id 'community-app-data'
    script_tag = soup.find("script", id="community-app-data", type="application/json")
    if script_tag and script_tag.string:
        data = json.loads(script_tag.string)
        # The group data is in data['members']
        for group in data.get("members", []):
            group_id = group.get("id")
            if group_id:
                href = f"{group_id}"
                group_ids.append(href)
    else:
        print(
            "No script tag with id 'community-app-data' found or it contains no data."
        )

    return group_ids


def get_dict_with_attribute(list_of_dicts, attribute, value):
    # Loop through each dictionary in the list
    for dictionary in list_of_dicts:
        # logging.warning(dictionary)
        # if attribute in dictionary:
        # logging.warning(dictionary[attribute])
        # Check if the attribute exists in the dictionary and has the specified value
        if attribute in dictionary and dictionary[attribute] == value:
            return dictionary  # Return the dictionary if found

    return None  # Return None if not found in any dictionary


def get_most_recent_date(date_local_resource, date_api):
    # logging.warning(f'{date_local_resource} , {date_api}')

    # Convert strings to datetime objects
    date_time_local_resource = datetime.datetime.fromisoformat(date_local_resource[:-1])
    date_time_api = datetime.datetime.fromisoformat(date_api[:-1])
    # logging.warning(f'{date_time_local_resource} , {date_time_api}')
    # Compare the datetime objects
    if date_time_local_resource > date_time_api:
        return False
    elif date_time_local_resource < date_time_api:
        return True
    else:
        return False


def update_resource(resource):
    single_resource = {}
    single_resource = {
        "title": resource["resource_title"],
        "abstract": resource["abstract"],
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
