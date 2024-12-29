import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from registration.models import UserModel
from registration.utils import create_jwt_token

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
class TestUserViewSet:
    def test_create_user_success(self, api_client):
        user_data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = api_client.post(reverse('register'), user_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data
        assert 'token' in response.data
        assert response.data['username'] == user_data['username']

    def test_create_user_duplicate_username(self, api_client):
        UserModel.objects.create(username='existinguser', password='password123')
        user_data = {
            'username': 'existinguser',
            'password': 'newpassword123'
        }
        response = api_client.post(reverse('register'), user_data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_user_invalid_data(self, api_client):
        invalid_user_data = {
            'username': '',
            'password': ''
        }
        response = api_client.post(reverse('register'), invalid_user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_user_token_generation(self, api_client):
        user_data = {
            'username': 'tokenuser',
            'password': 'testpassword123'
        }
        response = api_client.post(reverse('register'), user_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'token' in response.data
        
        created_user = UserModel.objects.get(username='tokenuser')
        assert response.data['token']
        assert len(response.data['token']) > 0

    def test_create_user_response_structure(self, api_client):
        user_data = {
            'username': 'structureuser',
            'password': 'testpassword123'
        }
        response = api_client.post(reverse('register'), user_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data
        assert 'username' in response.data
        assert 'token' in response.data

    def test_create_user_password_handling(self, api_client):
        user_data = {
            'username': 'passworduser',
            'password': 'testpassword123'
        }
        response = api_client.post(reverse('register'), user_data)
        assert response.status_code == status.HTTP_201_CREATED
        
        created_user = UserModel.objects.get(username='passworduser')
        assert created_user.password == user_data['password']
        assert len(created_user.password) > 0

    def test_create_user_with_long_username(self, api_client):
        user_data = {
            'username': 'a' * 101,
            'password': 'testpassword123'
        }
        response = api_client.post(reverse('register'), user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST