from cms.models.pluginmodel import CMSPlugin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from pyzotero import zotero
from hs_restclient import HydroShare, HydroShareAuthBasic
import requests

# from datetime import datetime

import datetime
import uuid
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)


class HydroShareResource(CMSPlugin):
    title = models.CharField(max_length=200, default="resource title")
    subtitle = models.CharField(max_length=200, default="resource subtitle")
    image = models.CharField(max_length=200, default="https://picsum.photos/200")
    width = models.PositiveIntegerField(
        default=200, validators=[MinValueValidator(150), MaxValueValidator(400)]
    )
    height = models.PositiveIntegerField(
        default=200, validators=[MinValueValidator(150), MaxValueValidator(400)]
    )
    description = models.TextField(default="resource description")
    github_url = models.CharField(max_length=200, default="", blank=True)
    documentation_url = models.CharField(max_length=200, default="", blank=True)
    web_site_url = models.CharField(max_length=200, default="", blank=True)
    unique_identifier = models.UUIDField(default=uuid.uuid4, editable=False)


class HydroShareResourceList(CMSPlugin):
    user = models.CharField(max_length=200, default="", blank=True)
    password = models.CharField(max_length=200, default="", blank=True)
    placeholder_image = models.CharField(
        max_length=200, default="https://picsum.photos/200"
    )
    # width= models.PositiveIntegerField(default=200, validators=[MinValueValidator(150), MaxValueValidator(400)])
    # height=models.PositiveIntegerField(default=200, validators=[MinValueValidator(150), MaxValueValidator(400)])
    tags = models.CharField(max_length=200, default="")
    updated_version = models.IntegerField(default=0, editable=False)
    resources = models.JSONField(editable=False, default=dict)


class HydroLearnModulesList(CMSPlugin):
    organization = models.CharField(max_length=200, default="", blank=True)
    placeholder_image = models.CharField(
        max_length=200, default="https://picsum.photos/200"
    )
    updated_version = models.IntegerField(default=0, editable=False)
    modules = models.JSONField(editable=False, default=dict)


class ZoteroBibliographyResource(CMSPlugin):
    api_key = models.CharField(max_length=200, default="")
    library_type = models.CharField(max_length=200, default="")
    library_id = models.CharField(max_length=200, default="")
    collection_id = models.CharField(max_length=200, default="", blank=True)
    style = models.CharField(max_length=200, default="apa")
    html = models.JSONField(editable=False)
    unique_identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    updated_version = models.IntegerField(default=0, editable=False)
    link_of_library_or_collection = models.CharField(max_length=400, default="")


@receiver(pre_save, sender=ZoteroBibliographyResource)
def create_html_citations(sender, instance, *args, **kwargs):
    params = {
        "include": "bib,data",
        "style": "apa",
        "sort": "date",
        "direction": "desc",
        "linkwrap": 1,
    }
    try:
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

        instance.html = publications_by_year
    except Exception as e:
        instance.html = {"Error": [f"The following error: {e}"]}


@receiver(post_save, sender=HydroLearnModulesList)
def fetch_hydrolearn_modules(sender, instance, *args, **kwargs):
    modules_list = []
    logger.warning("Fetching HydroLearn modules")
    try:
        URL = "https://edx.hydrolearn.org"
        client = requests.session()
        client.get(URL)  # sets cookie for CSRF
        csrftoken = client.cookies.get("csrftoken", "") or client.cookies.get(
            "csrf", ""
        )
        courses_url = f"{URL}/search/course_discovery/"

        login_data = {"csrfmiddlewaretoken": csrftoken}
        courses_response = client.post(
            courses_url, data=login_data, headers={"Referer": courses_url}
        )
        courses_list = courses_response.json()["results"]

        if instance.organization:

            def is_from_organization(course):
                return course["data"]["org"] == instance.organization

            courses_list = filter(is_from_organization, courses_list)
        for course in courses_list:
            course_data = course["data"]
            course_dict = {
                "course_title": course_data["content"]["display_name"],
                "course_url": f"{URL}/courses/{course_data.get('course')}/about",
                "course_image_url": (
                    f'{URL}{course_data.get("image_url")}'
                    if course_data.get("image_url", "") != ""
                    else ""
                ),
                "course_organization": course_data.get("org", ""),
                "course_code": course_data.get("number", ""),
                "course_weekly_effort": course_data.get("effort", ""),
                "course_description_content": course_data.get("content").get(
                    "short_description", ""
                ),
            }
            logger.warning(course_dict)

            modules_list.append(course_dict)

        instance.modules = modules_list
    except Exception as e:
        logger.warning(f"Error fetching HydroLearn modules: {e}")
        instance.modules = modules_list
