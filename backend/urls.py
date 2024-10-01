from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
import os

urlpatterns = [
    path("admin/", admin.site.urls),
    path("zotero_publications_app/", include("zotero_publications_app.urls")),
    path("hydrolearn_modules_app/", include("hydrolearn_modules_app.urls")),
    path("hydroshare_resources_app/", include("hydroshare_resources_app.urls")),
    path(
        "hydroshare_community_resources_app/",
        include("hydroshare_community_resources_app.urls"),
    ),
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
