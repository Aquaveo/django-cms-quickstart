from django.urls import re_path


from .views import base_view, hydrolearn_modules_view

urlpatterns = [
    re_path(r"^$", base_view, name="base"),
    re_path(
        r"^hydrolearn-modules-api/$",
        hydrolearn_modules_view,
        name="hydrolearn-modules-api",
    ),
]
