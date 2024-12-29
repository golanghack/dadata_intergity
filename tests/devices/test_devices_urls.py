import pytest
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from devices.views import DeviceModelViewSet, DeviceViewSet

@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def authenticated_client(db):
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpass')
    client.force_authenticate(user=user)
    return client

def test_device_model_list_url():
    url = reverse('device-model-list')
    assert url == '/device-models/'

    resolver_match = resolve('/device-models/')
    assert resolver_match.view_name == 'device-model-list'
    assert resolver_match.func.cls == DeviceModelViewSet

def test_device_model_list_methods():
    resolver_match = resolve('/device-models/')
    view_methods = resolver_match.func.actions
    
    assert 'get' in view_methods
    assert view_methods['get'] == 'list'
    assert 'post' in view_methods
    assert view_methods['post'] == 'create'

def test_device_list_url():
    url = reverse('device-list')
    assert url == '/devices/'

    resolver_match = resolve('/devices/')
    assert resolver_match.view_name == 'device-list'
    assert resolver_match.func.cls == DeviceViewSet

def test_device_list_methods():
    resolver_match = resolve('/devices/')
    view_methods = resolver_match.func.actions
    
    assert 'get' in view_methods
    assert view_methods['get'] == 'list'
    assert 'post' in view_methods
    assert view_methods['post'] == 'create'

@pytest.mark.django_db
def test_device_model_list_view(authenticated_client):
    url = reverse('device-model-list')
    response = authenticated_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_device_list_view(authenticated_client):
    url = reverse('device-list')
    response = authenticated_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_device_model_list_view_unauthorized(api_client):
    url = reverse('device-model-list')
    response = api_client.get(url)
    assert response.status_code == 401

@pytest.mark.django_db
def test_device_list_view_unauthorized(api_client):
    url = reverse('device-list')
    response = api_client.get(url)
    assert response.status_code == 401