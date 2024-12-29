
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config import settings
from config.docs import url_docs
from config.settings import ADMIN_PANEL_URL

urlpatterns = [
    path(f"{ADMIN_PANEL_URL}", admin.site.urls),
    path(r"ht/", include("health_check.urls")),
    path('', include('devices.urls')),
    path('token/', include('registration.urls')),
    
]

urlpatterns += url_docs

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
