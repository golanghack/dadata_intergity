from django.urls import path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

url_docs = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="docs",
    ),
    path(
        "api/v1/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
