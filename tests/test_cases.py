import json

from rest_framework import status
from rest_framework.test import APITransactionTestCase

from app.models import Lawyer


class TestCasesApi(APITransactionTestCase):
    fixtures = ["case.json"]

    def test_get_cases(self):
        response = self.client.get("/api/cases-api/")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {
                "id": 1,
                "is_active": True,
                "lawyer": 1,
                "client": 1,
                "case_closed_successfully": False,
                "article": "112",
                "description": "Test case",
            }
        ]
        assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED
        assert response.status_code != status.HTTP_404_NOT_FOUND

    def test_bad_request_case(self):
        response = self.client.post("/api/cases-api/", data={})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

    def test_create_case(self):
        request_body = {
            "is_active": True,
            "lawyer": 1,
            "client": 1,
            "case_closed_successfully": False,
            "article": "112",
            "description": "Test",
        }
        response = self.client.post("/api/cases-api/", json.dumps(request_body), content_type="application/json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.status_code != status.HTTP_400_BAD_REQUEST
        assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

    def test_update_case(self):
        request_body = {
            "is_active": True,
            "lawyer": 1,
            "client": 1,
            "case_closed_successfully": False,
            "article": "112",
            "description": "Update description",
        }
        response = self.client.put("/api/cases-api/1/", json.dumps(request_body), content_type="application/json")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["description"] == "Update description"
        assert response.status_code != status.HTTP_400_BAD_REQUEST
        assert response.status_code != status.HTTP_404_NOT_FOUND
        assert response.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

    def test_case_end_successfully(self):
        lawyer = Lawyer.objects.get(pk=1)
        request_body = {
            "is_active": False,
            "lawyer": 1,
            "client": 1,
            "case_closed_successfully": True,
            "article": "112",
            "description": "Test",
        }
        # Rating of lawyer before action
        # (successful_cases - unsuccessful_cases) * sqrt(1 + experience) = (20 - 5) * sqrt(1 + 5) = 36
        response_ratting_before = self.client.get("/api/lawyers-api/1/")
        assert lawyer.successful_cases == 20
        assert lawyer.unsuccessful_cases == 5
        assert response_ratting_before.json()["ratting"] == 36

        # Changing the status of a case
        response_case = self.client.put("/api/cases-api/1/", json.dumps(request_body), content_type="application/json")
        assert response_case.status_code == status.HTTP_200_OK
        assert response_case.json()["is_active"] is False
        assert response_case.json()["case_closed_successfully"] is True

        assert response_case.status_code != status.HTTP_400_BAD_REQUEST
        assert response_case.status_code != status.HTTP_404_NOT_FOUND
        assert response_case.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

        # Rating of lawyer after action
        # (successful_cases - unsuccessful_cases) * sqrt(1 + experience) = (21 - 5) * sqrt(1 + 5) = 39
        response_ratting_after = self.client.get("/api/lawyers-api/1/")
        assert response_ratting_after.json()["successful_cases"] == 21
        assert response_ratting_after.json()["unsuccessful_cases"] == 5
        assert response_ratting_after.json()["ratting"] == 39

    def test_is_active_true_and_ccs_true(self):
        request_body = {
            "is_active": True,
            "lawyer": 1,
            "client": 1,
            "case_closed_successfully": True,
            "article": "112",
            "description": "Test",
        }
        response = self.client.put("/api/cases-api/1/", json.dumps(request_body), content_type="application/json")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "You have not changed the status of the case, change its status to 'false'"

    def test_case_end_unsuccessfully(self):
        lawyer = Lawyer.objects.get(pk=1)
        request_body = {
            "is_active": False,
            "lawyer": 1,
            "client": 1,
            "case_closed_successfully": False,
            "article": "112",
            "description": "Test",
        }
        # Rating of lawyer before action
        # (successful_cases - unsuccessful_cases) * sqrt(1 + experience) = (20 - 5) * sqrt(1 + 5) = 36
        response_ratting_before = self.client.get("/api/lawyers-api/1/")
        assert lawyer.successful_cases == 20
        assert lawyer.unsuccessful_cases == 5
        assert response_ratting_before.json()["ratting"] == 36

        # Changing the status of a case
        response_case = self.client.put("/api/cases-api/1/", json.dumps(request_body), content_type="application/json")
        assert response_case.status_code == status.HTTP_200_OK
        assert response_case.json()["is_active"] is False
        assert response_case.json()["case_closed_successfully"] is False

        assert response_case.status_code != status.HTTP_400_BAD_REQUEST
        assert response_case.status_code != status.HTTP_404_NOT_FOUND
        assert response_case.status_code != status.HTTP_405_METHOD_NOT_ALLOWED

        # Rating of lawyer after action
        # (successful_cases - unsuccessful_cases) * sqrt(1 + experience) = (20 - 6) * sqrt(1 + 5) = 34
        response_ratting_after = self.client.get("/api/lawyers-api/1/")
        assert response_ratting_after.json()["successful_cases"] == 20
        assert response_ratting_after.json()["unsuccessful_cases"] == 6
        assert response_ratting_after.json()["ratting"] == 34
