from django.utils.translation import gettext_lazy as _
from .utils import (
    join_generators,
    get_group_ids,
    get_dict_with_attribute,
    get_most_recent_date,
    update_resource,
    filter_resources_list_by_resources_id,
    get_curated_resources,
)

from .models import (
    HydroShareCommunityResourcesList,
)
from hs_restclient import HydroShare, HydroShareAuthBasic
import logging
import json
from django.http import JsonResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)


def base_view(request):

    context = {}
    return render(request, "hydroshare-community-resources-base.html", context)


def hydroshare_community_resources_view(request):

    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)
    instance = HydroShareCommunityResourcesList.objects.get(id=body["instance_id"])
    is_curated = body["curated"]

    json_resources = {"resources": []}
    if instance.user != "" and instance.password != "":
        auth = HydroShareAuthBasic(username=instance.user, password=instance.password)
        hs = HydroShare(auth=auth)
    else:
        hs = HydroShare(prompt_auth=False)
    try:
        generators_rs = []
        group_ids = get_group_ids(instance.community_id)
        logger.warning(group_ids)
        for group_id in group_ids:
            generators_rs.append(hs.resources(group=group_id))

        resources_api = join_generators(generators_rs)
        if is_curated:
            logger.warning("curated is true")
            curated_ids = get_curated_resources(hs=hs)
            resources_api = filter_resources_list_by_resources_id(
                resources_api, curated_ids
            )
        resources_model = instance.resources.get("resources", [])

        for resource_api in resources_api:
            logger.warning(resource_api["resource_id"])
            matching_resource_model = get_dict_with_attribute(
                resources_model, "resource_id", resource_api["resource_id"]
            )

            # If resource found locally, then check last update date
            if matching_resource_model:
                is_recent_date = get_most_recent_date(
                    matching_resource_model["date_last_updated"],
                    resource_api["date_last_updated"],
                )
                if (
                    is_recent_date
                ):  # If the resource retrieved from api is more recent, then update resource
                    # logging.warning("resource has a more recent version")
                    single_resource = update_resource(resource_api, hs, instance)
                    # logging.warning(single_resource)
                    json_resources["resources"].append(single_resource)
                    instance.resources = json_resources

                else:  # resource is the same, then retrieve the resource saved locally
                    single_resource = matching_resource_model
                    json_resources["resources"].append(single_resource)
                    instance.resources = json_resources
            # If the resource is not here then create one
            else:
                single_resource = update_resource(resource_api, hs, instance)
                json_resources["resources"].append(single_resource)

                instance.resources = json_resources

        instance.save(update_fields=["resources"])
        return JsonResponse(json_resources)

    except Exception as e:
        logging.warning(e)
        instance.resources = {"Error": [f"The following error: {e}"]}
