from django.test import TestCase, RequestFactory
from django.test import Client

from health_appointment.util.create_system import create_system
from health_appointment.models.patient_model import Patient
from health_appointment.models.doctor_model import Doctor


class TestPatientHomeView(TestCase):
    def setUp(self) -> None:
        create_system()
        self.client = Client()
        self.patient_id = str(Patient.objects.all()[0].user_id)
        
    def test_get(self) -> None:
        url = f'/health_appointment/patient_home/{self.patient_id}/'
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200
        )


class TestSelectIllnessView(TestCase):
    def setUp(self) -> None:
        create_system()
        self.factory = RequestFactory()
        self.client = Client()
        self.patient_id = str(Patient.objects.all()[0].user_id)
        
    def test_get(self) -> None:
        request = f'/health_appointment/select/?user_id={self.patient_id}&Make+appointments='
        response = self.client.get(request)
        self.assertEqual(
            response.status_code,
            200
        )
        
        
class TestCreateAppointmentView(TestCase):
    def setUp(self) -> None:
        create_system()
        self.factory = RequestFactory()
        self.client = Client()
        self.patient_id = str(Patient.objects.all()[0].user_id)
        self.doctor_id = str(Doctor.objects.all()[0].user_id)
        
    def test_get(self) -> None:
        reuqest = f'/health_appointment/create_appointment_success/?illnesses=1&illness_category=1&user_id={self.patient_id}&doctor_id={self.doctor_id}&appointment_time_slot=21-12-15-08-00%2C21-12-15-08-30'
        response = self.client.get(
            reuqest
        )
        self.assertEqual(
            response.status_code,
            302
        )

class TestCheckAvailableAppointmentView(TestCase):
    def setUp(self) -> None:
        create_system()
        self.client = Client()
        self.patient_id = str(Patient.objects.all()[0].user_id)
        
    def test_get(self) -> None:
        request = f'/health_appointment/create_appointment/?csrfmiddlewaretoken=PftmkwMu3kIM0ITm1oB0yoLETzCS1rlRwGiTf0CwzCo7arVkQ0ZAfiMRHj5nl2sP&user_id={self.patient_id}&category=1&illness=1'
        response = self.client.get(request)
        
        self.assertEqual(
            response.status_code,
            200
        )