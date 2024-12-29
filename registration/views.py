from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from registration.models import UserModel
from registration.serializers import UserSerializer
from registration.utils import create_jwt_token


class UserViewSet(ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        request=UserSerializer,
        responses={
            status.HTTP_201_CREATED: UserSerializer,
        },
        tags=["Token"],
    )
    def create(self, request, *args, **kwargs):
        """
        Generate token from user uuid
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        uuid_user = user.id
        token_for_user = create_jwt_token(uuid_user)
        response = serializer.data
        response["token"] = token_for_user
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    

