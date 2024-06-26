from django.urls import re_path


from .views import (
    base_view,
    publications_view,
    get_items_number,
    initialize_publications_view,
)

urlpatterns = [
    re_path(r"^$", base_view, name="base"),
    re_path(
        r"^zotero-publications-api/$", publications_view, name="zotero-publications-api"
    ),
    re_path(r"^get-items-count/$", get_items_number, name="get-items-count"),
    re_path(
        r"^init-publications/$", initialize_publications_view, name="init-publications"
    ),
]
