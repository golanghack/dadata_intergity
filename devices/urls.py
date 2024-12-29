from django.urls import path

from devices.views import DeviceModelViewSet, DeviceViewSet

device_model_list = DeviceModelViewSet.as_view({'get': 'list', 'post': 'create'})
device_list = DeviceViewSet.as_view({'get': 'list', 'post': 'create'})

urlpatterns = [
    path('device-models/', device_model_list, name='device-model-list'),
    path('devices/', device_list, name='device-list'),
]