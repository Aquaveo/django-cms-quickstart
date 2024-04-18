from django.shortcuts import render
from django.http import JsonResponse
import logging
import json
import requests
from hs_restclient import HydroShare

logger = logging.getLogger(__name__)


def base_view(request):

    context = {}
    return render(request, "hydrolearn-modules-base.html", context)


## let's filter the modules using the HydroShare API
def filter_modules_view_using_hydroshare(tag):

    hs = HydroShare(prompt_auth=False)
    filter_list = []
    try:
        # let's call the resources
        resources = hs.resources(subject=tag)
        for resource in resources:
            logger.warning(f"{resource}")

            filter_list.append(resource["resource_title"])

    except Exception as e:
        logger.warning(f"Error fetching HydroLearn modules: {e}")
        filter_list = []

    return filter_list


def hydrolearn_modules_view(request):

    # This dictionary can pass variables to the template.
    logging.warning("hydrolearn_modules_view")
    hl_modules = {}
    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)
    instance = {
        "tag_filter": body["tag_filter"],
    }
    modules_list = []

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

            modules_list.append(course_dict)

        filter_hs_list = filter_modules_view_using_hydroshare(instance["tag_filter"])
        filtered_modules_list = [
            module
            for module in modules_list
            if module["course_title"] in filter_hs_list
        ]

        hl_modules["modules"] = filtered_modules_list
    except Exception as e:
        logger.warning(f"Error fetching HydroLearn modules: {e}")
        hl_modules["modules"] = modules_list

    return JsonResponse(hl_modules)
