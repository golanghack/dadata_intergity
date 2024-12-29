from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.tokens import AccessToken

from registration.models import UserModel


def create_jwt_token(user_uuid):
    try:
        user = UserModel.objects.get(id=user_uuid)  
    except UserModel.DoesNotExist:
        raise NotFound("Пользователь не найден")  
    token = AccessToken.for_user(user)  
    return str(token) 