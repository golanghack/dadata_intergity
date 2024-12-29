from rest_framework import serializers

from devices.models import Device, DeviceModel


class DeviceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceModel
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

