from rest_framework import serializers

from registration.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'


    def create(self, validated_data):
        user = UserModel.objects.create(**validated_data)
        return user