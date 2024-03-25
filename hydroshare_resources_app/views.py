from django.utils.translation import gettext_lazy as _
from .utils import get_dict_with_attribute, get_most_recent_date, update_resource

from .models import (
    HydroShareResourcesList,
)
from hs_restclient import HydroShare, HydroShareAuthBasic
import logging
import json
from django.http import JsonResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)


def base_view(request):

    context = {}
    return render(request, "hydroshare-resources-base.html", context)


def hydroshare_resources_view(request):

    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)

    instance = HydroShareResourcesList.objects.get(id=body["instance_id"])
    # logger.warning(instance.updated_version)
    keywords = []
    json_resources = {"resources": []}
    # logging.warning(instance.user,instance.password)
    if instance.tags:
        keywords = instance.tags.split(",")
        # logging.warning(keywords)
    if instance.user != "" and instance.password != "":
        auth = HydroShareAuthBasic(username=instance.user, password=instance.password)
        hs = HydroShare(auth=auth)
    else:
        hs = HydroShare(prompt_auth=False)

    try:
        # let's call the resources
        resources_api = hs.resources(subject=keywords)

        resources_model = instance.resources.get("resources", [])
        # logging.warning(resources_model)

        for resource_api in resources_api:
            # logging.warning(resource_api['resource_title'])

            matching_resource_model = get_dict_with_attribute(
                resources_model, "resource_id", resource_api["resource_id"]
            )
            # logging.warning("this is a matching_resource_model")
            # logging.warning(matching_resource_model)

            # If resource found locally, then check last update date
            if matching_resource_model:
                is_recent_date = get_most_recent_date(
                    matching_resource_model["date_last_updated"],
                    resource_api["date_last_updated"],
                )
                # logging.warning(is_recent_date)
                if (
                    is_recent_date
                ):  # If the resource retrieved from api is more recent, then update resource
                    # logging.warning("resource has a more recent version")
                    single_resource = update_resource(resource_api, hs, instance)
                    # logging.warning(single_resource)
                    json_resources["resources"].append(single_resource)
                    instance.resources = json_resources

                else:  # resource is the same, then retrive the resource saved locally
                    # logging.warning("resource is the same")

                    single_resource = matching_resource_model
                    json_resources["resources"].append(single_resource)
                    instance.resources = json_resources
            # If the resource is not here then create one
            else:
                # logging.warning(resource)
                # logging.warning("resource is new, creating now")
                single_resource = update_resource(resource_api, hs, instance)
                json_resources["resources"].append(single_resource)

                instance.resources = json_resources
        # logging.warning(json_resources)

        instance.save(update_fields=["resources"])
        return JsonResponse(json_resources)

    except Exception as e:
        instance.resources = {"Error": [f"The following error: {e}"]}
