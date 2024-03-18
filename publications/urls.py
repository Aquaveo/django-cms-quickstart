from django.urls import re_path


from .views import base_view, publications_view

urlpatterns = [
    re_path(r"^publications-api/$", publications_view, name="publications"),
]
