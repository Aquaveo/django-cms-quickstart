from cms.models.pluginmodel import CMSPlugin
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db import models
from pyzotero import zotero
from hs_restclient import HydroShare, HydroShareAuthBasic

# from datetime import datetime

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
    logger.warning(instance.updated_version)
    keywords = []
    json_resources = {
        'list_resources': []
    }
    # logging.warning(instance.user,instance.password)
    if instance.tags:
        keywords = instance.tags.split(',')
        # logging.warning(keywords)
    if instance.user != '' and instance.password != '':
        auth = HydroShareAuthBasic(username=instance.user, password=instance.password)
        hs = HydroShare(auth=auth)
    else:
        hs = HydroShare(prompt_auth=False)

    try:
        # let's call the resources
        resources_api = hs.resources(subject=keywords,types="ToolResource")
        resources_model = instance.resources.get('list_resources',[])
        logging.warning(resources_model)

        for resource_api in resources_api:
            logging.warning(resource_api['resource_title'])

            matching_resource_model = get_dict_with_attribute(resources_model, 'resource_id', resource_api['resource_id'])
            logging.warning(matching_resource_model)
            
            # If resource found locally, then check last update date
            if matching_resource_model:
                is_recent_date = get_most_recent_date(matching_resource_model['date_last_updated'],resource_api['date_last_updated'])
                logging.warning(is_recent_date)
                if is_recent_date : # If the resource retrieved from api is more recent, then update resource
                    logging.warning("resource has a more recent version")
                    single_resource = update_resource(resource_api,hs,instance)
                    # logging.warning(single_resource)
                    json_resources['list_resources'].append(single_resource)
                    instance.resources = json_resources

                else: # resource is the same, then retrive the resource saved locally
                    logging.warning("resource is the same")

                    single_resource = matching_resource_model
                    json_resources['list_resources'].append(single_resource)
                    instance.resources = json_resources
            # If the resource is not here then create one
            else:
                # logging.warning(resource)
                logging.warning("resource is new, creating now")
                single_resource = update_resource(resource_api,hs,instance)
                json_resources['list_resources'].append(single_resource)

                instance.resources = json_resources

    except Exception as e:
        instance.resources = {
            "Error":[
                f'The following error: {e}'
            ]
        }

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
    logging.warning(f'{date_local_resource} , {date_api}')

    # Convert strings to datetime objects
    date_time_local_resource = datetime.datetime.fromisoformat(date_local_resource[:-1])
    date_time_api = datetime.datetime.fromisoformat(date_api[:-1])
    logging.warning(f'{date_time_local_resource} , {date_time_api}')
    # Compare the datetime objects
    if date_time_local_resource > date_time_api:
        return False
    elif date_time_local_resource < date_time_api:
        return True
    else:
        return False

def update_resource(resource,hs,instance):
    science_metadata_json = hs.getScienceMetadata(resource['resource_id'])
    # logging.warning(science_metadata_json)

    single_resource={}
    image_url = science_metadata_json.get('app_icon',instance.placeholder_image).get('value',instance.placeholder_image)
    web_site_url = science_metadata_json.get('app_home_page_url','').get('value','')
    github_url = science_metadata_json.get('source_code_url','').get('value','')
    help_page_url = science_metadata_json.get('help_page_url','').get('value','')

    if image_url == '':
        image_url = instance.placeholder_image
    
    single_resource={
        'title':resource['resource_title'],
        'abstract':resource['abstract'],
        'github_url': github_url,
        'image': image_url,
        'web_site_url': web_site_url,
        'documentation_url': help_page_url,
        'unique_identifier': f'{uuid.uuid4()}',
        'resource_id':resource['resource_id'],
        'date_last_updated': resource['date_last_updated']
    }
    return single_resource