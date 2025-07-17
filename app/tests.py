from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Appointment

class AppointmentAPITest(APITestCase):
    def setUp(self):
        # Crée un utilisateur médecin et quelques RDV
        self.doc = User.objects.create_user('doc', password='pwd', role=User.Roles.MEDECIN)
        Appointment.objects.create(patient=self.doc, doctor=self.doc,
                                   scheduled_time='2025-07-20T10:00:00Z')
        self.client.force_authenticate(self.doc)

    def test_list_appointments(self):
        url = reverse('appointment-list')  # ou le nom de ta route DRF
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsInstance(resp.json(), list)

    def test_create_appointment_forbidden_to_doctor(self):
        url = reverse('appointment-list')
        data = {'doctor': self.doc.id, 'scheduled_time': '2025-07-21T11:00:00Z'}
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_available_slots(self):
        url = reverse('appointment-available-slots')
        resp = self.client.get(url + f'?doctor={self.doc.id}&date=2025-07-20')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(resp.json(), list))
