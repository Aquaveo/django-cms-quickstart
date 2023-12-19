from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from .models import HydroShareResource,HydroShareResourceList,ZoteroBibliographyResource
import logging
from hs_restclient import HydroShare, HydroShareAuthBasic
import uuid

# from datetime import datetime

import datetime

logger = logging.getLogger(__name__)

@plugin_pool.register_plugin
class HydroShareResourcePlugin(CMSPluginBase):
    model = HydroShareResource
    name = _("HydroShare Resource Plugin")
    render_template = "hydroshare_resource_template.html"
    cache = False
    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context


@plugin_pool.register_plugin
class HydroShareResourceListPlugin(CMSPluginBase):
    model = HydroShareResourceList
    name = _("HydroShare Resource List Plugin")
    render_template = "hydroshare_list_resources.html"
    cache = False
    def render(self, context, instance, placeholder):
        create_hydroshare_resources(instance)
        # instance.updated_version = instance.updated_version + 1
        # instance.save(update_fields=['updated_version'])
        context = super().render(context, instance, placeholder)
        return context

@plugin_pool.register_plugin
class ZoteroBibliographyResourcePlugin(CMSPluginBase):
    model = ZoteroBibliographyResource
    name = _("Zotero Citation Resource Plugin")
    render_template = "zotero_bibliography.html"
    cache = False

    #This is key in order to call the API every time the page renders
    #The instance.save calls the pre_save signal which makes the call of the API
    def render(self, context, instance, placeholder):
        instance.updated_version = instance.updated_version + 1
        instance.save(update_fields=['updated_version'])
        context = super().render(context, instance, placeholder)
        return context
      

def create_hydroshare_resources(instance):
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
        resources_api = hs.resources(subject=keywords)
        #how about "nwm_portal_app" for "Tool Resources that are part of the apps page, and how about "nwm_portal_data" for Data Resources?
        resources_model = instance.resources.get('list_resources',[])
        # logging.warning(resources_model)

        for resource_api in resources_api:
            logging.warning(resource_api['resource_title'])

            matching_resource_model = get_dict_with_attribute(resources_model, 'resource_id', resource_api['resource_id'])
            # logging.warning(matching_resource_model)
            
            # If resource found locally, then check last update date
            if matching_resource_model:
                is_recent_date = get_most_recent_date(matching_resource_model['date_last_updated'],resource_api['date_last_updated'])
                # logging.warning(is_recent_date)
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
        instance.save(update_fields=['resources'])
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