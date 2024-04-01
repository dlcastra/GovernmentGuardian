import json

from rest_framework import status
from rest_framework.test import APITransactionTestCase


class TestLawyerApi(APITransactionTestCase):
    fixtures = ["lawyer.json"]

    def test_get_lawyer_api(self):
        response = self.client.get("/api/lawyers-api/")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {
                "id": 1,
                "name": "Martin",
                "surname": "Sad",
                "birthdate": "1980-06-10",
                "experience": 5,
                "successful_cases": 20,
                "unsuccessful_cases": 5,
                "price": 2000,
                "characterization": "Lucky",
                "ratting": 36,
                "active_cases": [],
            }
        ]

        assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

    def test_lawyer_bad_request(self):
        response = self.client.post("/api/lawyers-api/", {})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

    def test_lawyer_not_found(self):
        response = self.client.get("/api/lawyers-api/22222/")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

    def test_created_lawyer(self):
        request_body = {
            "name": "Li",
            "surname": "Sad",
            "birthdate": "1980-01-11",
            "experience": 8,
            "successful_cases": 50,
            "unsuccessful_cases": 15,
            "price": 5000,
            "characterization": "Lucky man",
        }
        response = self.client.post("/api/lawyers-api/", json.dumps(request_body), content_type="application/json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.status_code != status.HTTP_400_BAD_REQUEST
        assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

    def test_updated_lawyer(self):
        request_body = {
            "name": "Martin",
            "surname": "Sad",
            "birthdate": "1980-06-10",
            "experience": 5,
            "successful_cases": 20,
            "unsuccessful_cases": 5,
            "price": 2000,
            "characterization": "unLucky",
        }
        response = self.client.put("/api/lawyers-api/1/", json.dumps(request_body), content_type="application/json")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["characterization"] == "unLucky"
        assert response.status_code != status.HTTP_400_BAD_REQUEST
        assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED
