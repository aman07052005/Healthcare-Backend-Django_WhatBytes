from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

class PatientAccessTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="one@example.com", email="one@example.com",
                                             name="User One", password="StrongPassword123!")
        self.other = User.objects.create_user(username="two@example.com", email="two@example.com",
                                              name="User Two", password="StrongPassword123!")
        self.client.force_authenticate(self.user)

    def test_patient_is_owned_by_creator(self):
        response = self.client.post("/api/patients/", {
            "name": "Patient One", "age": 34, "gender": "Female"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        patient_id = response.data["id"]
        self.client.force_authenticate(self.other)
        response = self.client.get(f"/api/patients/{patient_id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
