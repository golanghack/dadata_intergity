import pytest
from django.contrib.auth.models import User
from devices.models import Device, DeviceModel
from devices.serializers import DeviceModelSerializer, DeviceSerializer

@pytest.mark.django_db
class TestDeviceModelSerializer:
    def test_valid_serialization(self):
        device_model = DeviceModel.objects.create(name="Model A", description="Description A")
        serializer = DeviceModelSerializer(device_model)
        assert serializer.data == {
            'id': device_model.id,
            'name': "Model A",
            'description': "Description A",
        }

    def test_valid_deserialization(self):
        data = {'name': "Model B", 'description': "Description B"}
        serializer = DeviceModelSerializer(data=data)
        assert serializer.is_valid()
        device_model = serializer.save()
        assert device_model.name == "Model B"
        assert device_model.description == "Description B"

    def test_invalid_deserialization(self):
        data = {'name': ""}
        serializer = DeviceModelSerializer(data=data)
        assert not serializer.is_valid()
        assert 'name' in serializer.errors


@pytest.mark.django_db
class TestDeviceSerializer:
    def test_valid_serialization(self):
        user = User.objects.create(username="testuser")
        device_model = DeviceModel.objects.create(name="Model A", description="Description A")
        device = Device.objects.create(
            address="123 Main St",
            name="Device 1",
            ip_address="192.168.1.1",
            author=user,
            device_model=device_model,
            comment="Test comment"
        )
        serializer = DeviceSerializer(device)
        assert serializer.data == {
            'id': device.id,
            'address': "123 Main St",
            'name': "Device 1",
            'ip_address': "192.168.1.1",
            'author': user.id,
            'device_model': device_model.id,
            'comment': "Test comment",
        }

    def test_valid_deserialization(self):
        user = User.objects.create(username="testuser")
        device_model = DeviceModel.objects.create(name="Model A", description="Description A")
        data = {
            'address': "456 Another St",
            'name': "Device 2",
            'ip_address': "192.168.1.2",
            'author': user.id,
            'device_model': device_model.id,
            'comment': "Another comment"
        }
        serializer = DeviceSerializer(data=data)
        assert serializer.is_valid()
        device = serializer.save()
        assert device.address == "456 Another St"
        assert device.name == "Device 2"
        assert device.ip_address == "192.168.1.2"
        assert device.author == user
        assert device.device_model == device_model
        assert device.comment == "Another comment"

    def test_invalid_deserialization(self):
        data = {'address': "", 'name': "", 'ip_address': "invalid_ip"}
        serializer = DeviceSerializer(data=data)
        assert not serializer.is_valid()
        assert 'address' in serializer.errors
        assert 'name' in serializer.errors
        assert 'ip_address' in serializer.errors