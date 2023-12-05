from cms.models.pluginmodel import CMSPlugin
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db import models
from pyzotero import zotero
from hs_restclient import HydroShare, HydroShareAuthBasic
import hsclient


import datetime
import uuid
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

class HydroShareResource(CMSPlugin):
    title = models.CharField(max_length=200, default='resource title')
    subtitle = models.CharField(max_length=200, default='resource subtitle')
    image = models.CharField(max_length=200, default='https://picsum.photos/200')
    width= models.PositiveIntegerField(default=200, validators=[MinValueValidator(150), MaxValueValidator(400)])
    height=models.PositiveIntegerField(default=200, validators=[MinValueValidator(150), MaxValueValidator(400)])
    description= models.TextField(default='resource description')
    github_url=models.CharField(max_length=200, default='', blank=True)
    documentation_url=models.CharField(max_length=200, default='', blank=True)
    web_site_url=models.CharField(max_length=200, default='', blank=True)
    unique_identifier=models.UUIDField(default=uuid.uuid4, editable=False)


class HydroShareResourceList(CMSPlugin):
    user = models.CharField(max_length=200, default='', blank=True)
    password = models.CharField(max_length=200, default='', blank=True)
    placeholder_image = models.CharField(max_length=200, default='https://picsum.photos/200')
    # width= models.PositiveIntegerField(default=200, validators=[MinValueValidator(150), MaxValueValidator(400)])
    # height=models.PositiveIntegerField(default=200, validators=[MinValueValidator(150), MaxValueValidator(400)])
    tags=models.CharField(max_length=200, default='')
    updated_version=models.IntegerField(default=0, editable=False)
    resources=models.JSONField(editable=False,default=dict)
    

class ZoteroBibliographyResource(CMSPlugin):
    api_key = models.CharField(max_length=200, default='')
    library_type=models.CharField(max_length=200, default='')
    library_id = models.CharField(max_length=200, default='')
    collection_id = models.CharField(max_length=200, default='', blank=True)
    style= models.CharField(max_length=200, default='apa')
    html=models.JSONField(editable=False)
    unique_identifier=models.UUIDField(default=uuid.uuid4, editable=False)
    updated_version=models.IntegerField(default=0, editable=False)
    link_of_library_or_collection = models.CharField(max_length=400, default='')
    
@receiver(pre_save, sender=ZoteroBibliographyResource)
def create_html_citations(sender, instance, *args, **kwargs):
    params = {
        'include': 'bib,data',
        'style': 'apa',
        'sort': 'date',
        'direction': 'desc',
        'linkwrap': 1
    }
    try:
        zot = zotero.Zotero(instance.library_id, instance.library_type, instance.api_key)
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
        instance.html = {
            "Error":[
                f'The following error: {e}'
            ]
        }


@receiver(pre_save, sender=HydroShareResourceList)
def create_hydroshare_resources(sender, instance, *args, **kwargs):
    keywords = []
    json_resources = {
        'list_resources': []
    }
    if instance.tags:
        keywords = instance.tags.split(',')
        # logging.warning(keywords)
    if instance.user != '' and instance.password != '':
        hscli = hsclient.HydroShare(instance.user, instance.password)
    else:
        hscli = hsclient.HydroShare()

    try:
        for resource in hscli.search(subject=keywords):
            single_resource={}
            # addtional_metadata_dict = resource.get('metadata','').get('additional_metadata','')
            addtional_metadata_dict = {}
            addtional_metadata_dict = extract_urls(resource.abstract)

            # addtional_metadata_dict = hscli.resource(resource.resource_id).metadata.additional_metadata
            image_url = addtional_metadata_dict.get('image_url', instance.placeholder_image)

            if image_url == '':
                image_url = instance.placeholder_image
            
            single_resource={
                'title':resource.resource_title,
                'abstract': addtional_metadata_dict.get('abstract_text',resource.abstract),
                'github_url': addtional_metadata_dict.get('github_url',''),
                'image': image_url,
                'web_site_url': addtional_metadata_dict.get('website_url',''),
                'unique_identifier': f'{uuid.uuid4()}'
            }
            # logging.warning(single_resource)

            json_resources['list_resources'].append(single_resource)
        instance.resources = json_resources
    except Exception as e:
        instance.resources = {
            "Error":[
                f'The following error: {e}'
            ]
        }


def extract_urls(text: str) -> dict:
    lines = text.split('\n')
    url_mapping = {}
    for line in lines:
        parts = line.split(': ')
        if len(parts) == 2:
            key, value = parts
            url_mapping[key] = value
    return {
        'abstract_text': lines[0],  
        'image_url': url_mapping.get('image_url', ''),
        'github_url': url_mapping.get('github_url', ''),
        'website_url': url_mapping.get('website_url', ''),
        'documentation': url_mapping.get('documentation', '')
    }

