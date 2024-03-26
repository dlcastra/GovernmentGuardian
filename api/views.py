from rest_framework import generics
from rest_framework.viewsets import GenericViewSet

from api.serializers import ClientSerializer, LawyerSerializer, CaseSerializer
from app.models import Client, Lawyer, Case


class ClientViewSet(generics.ListAPIView, generics.RetrieveAPIView, generics.CreateAPIView, GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]


class LawyerViewSet(generics.ListAPIView, generics.RetrieveAPIView, generics.CreateAPIView, GenericViewSet):
    queryset = Lawyer.objects.all()
    serializer_class = LawyerSerializer

    # permission_classes = [IsAuthenticatedOrReadOnly]
    def update(self, request, *args, **kwargs): ...


class CaseViewSet(generics.ListAPIView, generics.RetrieveAPIView, generics.CreateAPIView, GenericViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer