from django.urls import re_path


from .views import base_view, hydroshare_community_resources_view

urlpatterns = [
    re_path(r"^$", base_view, name="base"),
    re_path(
        r"^update-hydroshare-community-resources/$",
        hydroshare_community_resources_view,
        name="update-hydroshare-community-resources",
    ),
]
