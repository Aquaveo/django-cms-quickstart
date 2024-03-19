from django.urls import re_path


from .views import base_view, publications_view

urlpatterns = [
    re_path(r"^$", base_view, name="base"),
    re_path(
        r"^zotero-publications-api/$", publications_view, name="zotero-publications-api"
    ),
]
