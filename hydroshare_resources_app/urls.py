from django.urls import re_path


from .views import base_view, hydroshare_resources_view

urlpatterns = [
    re_path(r"^$", base_view, name="base"),
    re_path(
        r"^update-hydroshare-resources/$",
        hydroshare_resources_view,
        name="update-hydroshare-resources",
    ),
]
