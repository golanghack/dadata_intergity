import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from devices.models import Device, DeviceModel
from devices.serializers import DeviceSerializer, DeviceModelSerializer

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def authenticated_client(db, user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def device_model(db):
    return DeviceModel.objects.create(
        name='Test Model', 
        description='Test Description'
    )

@pytest.mark.django_db
class TestDeviceModelViewSet:
    def test_list_device_models(self, authenticated_client):
        DeviceModel.objects.create(name='Test Model', description='Test Description')
        DeviceModel.objects.create(name='Another Model', description='Another Description')
        response = authenticated_client.get('/device-models/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_create_device_model(self, authenticated_client):
        device_model_data = {
            'name': 'Test Model',
            'description': 'Test Description'
        }
        response = authenticated_client.post('/device-models/', device_model_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == device_model_data['name']
        assert response.data['description'] == device_model_data['description']

    def test_create_device_model_invalid_data(self, authenticated_client):
        invalid_data = {'name': ''}
        response = authenticated_client.post('/device-models/', invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_device_models_unauthorized(self, api_client):
        response = api_client.get('/device-models/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestDeviceViewSet:
    def test_list_devices(self, authenticated_client, user, device_model):
        Device.objects.create(
            name='Device 1', 
            address='Address 1', 
            ip_address='192.168.1.1', 
            author=user, 
            device_model=device_model
        )
        Device.objects.create(
            name='Device 2', 
            address='Address 2', 
            ip_address='192.168.1.2', 
            author=user, 
            device_model=device_model
        )
        response = authenticated_client.get('/devices/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_create_device(self, authenticated_client, user, device_model):
        device_data = {
            'name': 'Test Device',
            'address': 'Test Address',
            'ip_address': '192.168.1.1',
            'author': user.id,
            'device_model': device_model.id,
            'comment': 'Test Comment'
        }
        response = authenticated_client.post('/devices/', device_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == device_data['name']
        assert response.data['address'] == device_data['address']
        assert response.data['ip_address'] == device_data['ip_address']

    def test_create_device_invalid_data(self, authenticated_client, user, device_model):
        invalid_data = {
            'name': '',
            'address': 'Test Address',
            'ip_address': 'invalid_ip',
            'author': user.id,
            'device_model': device_model.id
        }
        response = authenticated_client.post('/devices/', invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_device_unauthorized(self, api_client, user, device_model):
        device_data = {
            'name': 'Test Device',
            'address': 'Test Address',
            'ip_address': '192.168.1.1',
            'author': user.id,
            'device_model': device_model.id,
            'comment': 'Test Comment'
        }
        response = api_client.post('/devices/', device_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_devices_unauthorized(self, api_client):
        response = api_client.get('/devices/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED