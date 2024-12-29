import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from devices.models import DeviceModel, Device

@pytest.mark.django_db
class TestDeviceModel:
    def test_create_device_model(self):
        device_model = DeviceModel.objects.create(
            name='Test Model',
            description='Test Description'
        )
        
        assert device_model.name == 'Test Model'
        assert device_model.description == 'Test Description'
        assert str(device_model) == 'Test Model'

    def test_device_model_max_length(self):
        device_model = DeviceModel.objects.create(
            name='A' * 100,
            description='Test Description'
        )
        
        assert len(device_model.name) == 100

    def test_device_model_blank_description(self):
        device_model = DeviceModel.objects.create(
            name='Test Model'
        )
        
        assert device_model.description == ''

@pytest.mark.django_db
class TestDevice:
    def setup_method(self):
        self.user = User.objects.create_user(username='testuser')
        self.device_model = DeviceModel.objects.create(
            name='Test Model', 
            description='Test Description'
        )

    def test_create_device(self):
        device = Device.objects.create(
            address='Test Address',
            name='Test Device',
            ip_address='192.168.1.1',
            author=self.user,
            device_model=self.device_model,
            comment='Test Comment'
        )
        
        assert device.address == 'Test Address'
        assert device.name == 'Test Device'
        assert device.ip_address == '192.168.1.1'
        assert device.author == self.user
        assert device.device_model == self.device_model
        assert device.comment == 'Test Comment'
        assert str(device) == 'Test Device (192.168.1.1)'

    def test_device_null_author_and_model(self):
        device = Device.objects.create(
            address='Test Address',
            name='Test Device',
            ip_address='192.168.1.1'
        )
        
        assert device.author is None
        assert device.device_model is None

    def test_device_max_length_fields(self):
        device = Device.objects.create(
            address='A' * 255,
            name='A' * 100,
            ip_address='192.168.1.1',
            author=self.user,
            device_model=self.device_model
        )
        
        assert len(device.address) == 255
        assert len(device.name) == 100

    def test_device_blank_comment(self):
        device = Device.objects.create(
            address='Test Address',
            name='Test Device',
            ip_address='192.168.1.1',
            author=self.user,
            device_model=self.device_model
        )
        
        assert device.comment == ''

    def test_device_str_method(self):
        device = Device.objects.create(
            address='Test Address',
            name='Test Device',
            ip_address='192.168.1.1',
            author=self.user,
            device_model=self.device_model
        )
        
        assert str(device) == 'Test Device (192.168.1.1)'

    def test_device_ip_address_validation(self):
        with pytest.raises(ValidationError):
            invalid_device = Device(
                address='Test Address',
                name='Test Device',
                ip_address='invalid_ip',
                author=self.user,
                device_model=self.device_model
            )
            invalid_device.full_clean()