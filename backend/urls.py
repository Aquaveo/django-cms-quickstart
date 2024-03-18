from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
import os

urlpatterns = [
    path("admin/", admin.site.urls),
    path("publications/", include("publications.urls")),
]

# if settings.DEBUG:
#     urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

urlpatterns.append(path("", include("cms.urls")))

prefix_to_path = os.environ.get("PREFIX_TO_PATH")
if prefix_to_path:
    urlpatterns = [re_path(rf"^{prefix_to_path}/", include(urlpatterns))]

# the new django admin sidebar is bad UX in django CMS custom admin views.
# admin.site.enable_nav_sidebar = False
