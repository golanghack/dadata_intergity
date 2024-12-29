from django.urls import path

from registration.views import UserViewSet

urlpatterns = [
    path("", UserViewSet.as_view({"post": "create"}), name="register"),
]
