import pytest
import uuid
from registration.models import UserModel
from registration.serializers import UserSerializer

@pytest.mark.django_db
class TestUserSerializer:
    def test_valid_serialization(self):
        user = UserModel.objects.create(username="testuser", password="password123")
        serializer = UserSerializer(user)
        assert serializer.data == {
            'id': str(user.id),
            'username': "testuser",
            'password': "password123",
        }

    def test_valid_deserialization(self):
        data = {'username': "newuser", 'password': "newpassword"}
        serializer = UserSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.save()
        assert user.username == "newuser"
        assert user.password == "newpassword"

    def test_create_user(self):
        data = {'username': "createuser", 'password': "createpassword"}
        serializer = UserSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.save()
        assert user.username == "createuser"
        assert user.password == "createpassword"
        assert isinstance(user.id, uuid.UUID)

    def test_invalid_deserialization(self):
        data = {'username': "", 'password': ""}
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        assert 'username' in serializer.errors
        assert 'password' in serializer.errors