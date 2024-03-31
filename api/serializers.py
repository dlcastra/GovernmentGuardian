from math import sqrt

from rest_framework import serializers

from app.models import Client, Lawyer, Case


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name", "surname", "birthdate", "phone", "email"]


class LawyerSerializer(serializers.ModelSerializer):
    ratting = serializers.SerializerMethodField()
    active_cases = serializers.SerializerMethodField()

    class Meta:
        model = Lawyer
        fields = [
            "id",
            "name",
            "surname",
            "birthdate",
            "experience",
            "successful_cases",
            "unsuccessful_cases",
            "price",
            "characterization",
            "ratting",
            "active_cases",
        ]

    @staticmethod
    def get_ratting(object: Lawyer):
        successful_cases = object.successful_cases
        unsuccessful_cases = object.unsuccessful_cases
        experience = object.experience
        ratting = (successful_cases - unsuccessful_cases) * sqrt(1 + experience)

        return int(ratting)

    @staticmethod
    def get_active_cases(obj):
        active_cases = obj.lawyer_cases.filter(is_active=True)
        serializer = CaseSerializer(active_cases, many=True)
        return serializer.data


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ["id", "is_active", "lawyer", "client", "case_closed_successfully", "article", "description"]
