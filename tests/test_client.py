from rest_framework import status
from rest_framework.test import APITransactionTestCase
import json


class TestClientApi(APITransactionTestCase):
    fixtures = ["client.json"]

    def test_get_client_api(self):
        response = self.client.get("/api/clients-api/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {
                "id": 1,
                "name": "John",
                "surname": "Doe",
                "birthdate": "2000-10-18",
                "phone": "+380661234209",
                "email": "john@gmail.com",
            }
        ]
        assert response.json() != []
        assert response.status_code != status.HTTP_301_MOVED_PERMANENTLY
        assert response.status_code != status.HTTP_404_NOT_FOUND
        assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

    def test_client_bad_request(self):
        response = self.client.post("/api/clients-api/", {})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.status_code != status.HTTP_201_CREATED
        assert response.status_code != status.HTTP_301_MOVED_PERMANENTLY

    def test_create_client(self):
        request_body = {
            "name": "Jon",
            "surname": "Doe",
            "birthdate": "2011-10-18",
            "phone": "+380661234209",
            "email": "email@gmail.com",
        }
        response = self.client.post("/api/clients-api/", json.dumps(request_body), content_type="application/json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.status_code != status.HTTP_301_MOVED_PERMANENTLY
        assert response.status_code != status.HTTP_400_BAD_REQUEST
        assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

    def test_update_client(self):
        update_data = {
            "name": "Max",
            "surname": "Doe",
            "birthdate": "2000-10-18",
            "phone": "+380661234209",
            "email": "newjohn@gmail.com",
        }
        response = self.client.put("/api/clients-api/1/", json.dumps(update_data), content_type="application/json")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "Max"
        assert response.json()["email"] == "newjohn@gmail.com"

        assert response.status_code != status.HTTP_301_MOVED_PERMANENTLY
        assert response.status_code != status.HTTP_400_BAD_REQUEST
        assert response.status_code != status.HTTP_404_NOT_FOUND
        assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

    def test_method_not_allowed(self):
        response = self.client.delete("/api/clients-api/1/")

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response.status_code != status.HTTP_204_NO_CONTENT
