from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers import ClientSerializer, LawyerSerializer, CaseSerializer
from app.models import Client, Lawyer, Case


class ClientViewSet(
    generics.ListAPIView, generics.RetrieveAPIView, generics.CreateAPIView, generics.UpdateAPIView, GenericViewSet
):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class LawyerViewSet(generics.ListAPIView, generics.RetrieveAPIView, generics.CreateAPIView, GenericViewSet):
    queryset = Lawyer.objects.all()
    serializer_class = LawyerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)


class CaseViewSet(generics.ListAPIView, generics.RetrieveAPIView, generics.CreateAPIView, GenericViewSet):
    queryset = Case.objects.filter(is_active=True)
    serializer_class = CaseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        lawyer = instance.lawyer
        _case_success = request.data.get("case_closed_successfully")
        _case_status = request.data["is_active"]
        if _case_success:
            if _case_status:
                return Response(
                    {"message": "You have not changed the status of the case, change its status to 'false'"}
                )
            else:
                instance.is_active = False
                lawyer.successful_cases += 1
                lawyer.save()

        elif _case_status is False and _case_success is False:
            lawyer.unsuccessful_cases += 1
            lawyer.save()

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)
