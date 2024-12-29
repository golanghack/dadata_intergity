import pytest
import uuid
from django.core.exceptions import ValidationError
from registration.models import UserModel

@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = UserModel.objects.create(
            username='testuser',
            password='testpassword'
        )
        assert user.username == 'testuser'
        assert user.password == 'testpassword'
        assert isinstance(user.id, uuid.UUID)

    def test_user_str_method(self):
        user = UserModel.objects.create(
            username='testuser',
            password='testpassword'
        )
        assert str(user) == 'testuser'

    def test_multiple_users_same_username(self):
        UserModel.objects.create(
            username='testuser',
            password='password1'
        )
        user2 = UserModel.objects.create(
            username='testuser',
            password='password2'
        )
        assert user2.username == 'testuser'
        assert UserModel.objects.filter(username='testuser').count() == 2

    def test_user_uuid_generation(self):
        user1 = UserModel.objects.create(
            username='user1',
            password='password1'
        )
        user2 = UserModel.objects.create(
            username='user2',
            password='password2'
        )
        assert user1.id != user2.id
        assert isinstance(user1.id, uuid.UUID)
        assert isinstance(user2.id, uuid.UUID)

    def test_username_max_length(self):
        long_username = 'a' * 101
        with pytest.raises(ValidationError):
            user = UserModel(
                username=long_username,
                password='testpassword'
            )
            user.full_clean()  

    def test_password_max_length(self):
        long_password = 'a' * 101 
        with pytest.raises(ValidationError):
            user = UserModel(
                username='testuser',
                password=long_password
            )
            user.full_clean()  

    def test_required_fields(self):
        with pytest.raises(ValidationError):
            user = UserModel(
                username='', 
                password='' 
            )
            user.full_clean()

    def test_user_update(self):
        user = UserModel.objects.create(
            username='originaluser',
            password='originalpassword'
        )
        user.username = 'updateduser'
        user.save()
        updated_user = UserModel.objects.get(id=user.id)
        assert updated_user.username == 'updateduser'

    def test_user_delete(self):
        user = UserModel.objects.create(
            username='usertoDelete',
            password='testpassword'
        )
        user_id = user.id
        user.delete()
        with pytest.raises(UserModel.DoesNotExist):
            UserModel.objects.get(id=user_id)