from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from devices.models import Device, DeviceModel
from devices.serializers import DeviceModelSerializer, DeviceSerializer


@extend_schema(
    request=DeviceModelSerializer,
    responses={
        201: DeviceModelSerializer,
        200: DeviceModelSerializer,
        404: 'Not Found',
    },
    tags=['DevicesModel'],
)
class DeviceModelViewSet(ModelViewSet):
    """
    API endpoint that allows device models to be viewed or edited.
    """
    queryset = DeviceModel.objects.all()
    serializer_class = DeviceModelSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    request=DeviceSerializer,
    responses={
        201: DeviceSerializer,
        200: DeviceSerializer,
        404: 'Not Found',
    },
    tags=['Devices'],
)
class DeviceViewSet(ModelViewSet):
    """
    API endpoint that allows devices to be viewed or edited.
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

