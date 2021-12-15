import uuid
from unittest.mock import patch

from django.test import TestCase
from django.test import Client

from pandas import Timestamp

from health_appointment.util.create_system import create_system
from health_appointment.models.user_model import User
from health_appointment.models.patient_model import Patient
from health_appointment.models.doctor_model import Doctor
from health_appointment.models.appointment_model import Appointment


def setup_helper():
    create_system()
    client = Client()
    patient_id = str(Patient.objects.all()[0].user_id)
    return client, patient_id


class TestHomeView(TestCase):
    def setUp(self) -> None:
        self.client, self.patient_id = setup_helper()
    
    def test_get(self) -> None:
        url = f'/health_appointment/home/'
        with patch.object(
            User,
            "get_user",
            return_value=Patient.objects.all()[0],
        ):
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                302
            )
        
        
class TestPatientHomeView(TestCase):
    def setUp(self) -> None:
        self.client, self.patient_id = setup_helper()
        
    def test_get(self) -> None:
        url = f'/health_appointment/patient_home/{self.patient_id}/'
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            200
        )


class TestSelectIllnessView(TestCase):
    def setUp(self) -> None:
        self.client, self.patient_id = setup_helper()
        
    def test_get(self) -> None:
        request = f'/health_appointment/select/?user_id={self.patient_id}&Make+appointments='
        response = self.client.get(request)
        self.assertEqual(
            response.status_code,
            200
        )
        
        
class TestCreateAppointmentView(TestCase):
    def setUp(self) -> None:
        self.client, self.patient_id = setup_helper()
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
        self.client, self.patient_id = setup_helper()
        
    def test_get(self) -> None:
        request = f'/health_appointment/create_appointment/?csrfmiddlewaretoken=PftmkwMu3kIM0ITm1oB0yoLETzCS1rlRwGiTf0CwzCo7arVkQ0ZAfiMRHj5nl2sP&user_id={self.patient_id}&category=1&illness=1'
        response = self.client.get(request)
        
        self.assertEqual(
            response.status_code,
            200
        )


class TestCancelAppointmentView(TestCase):
    def setUp(self) -> None:
        self.client, self.patient_id = setup_helper()
        self.doctor_id = str(Doctor.objects.all()[0].user_id)
        self.appointment = Appointment.objects.create(
            appointment_id=uuid.uuid4(),
            doctor_id=self.doctor_id,
            patient_id=self.patient_id,
            create_time=Timestamp(year=2021, month=12, day=15, hour=10, minute=0),
            begin_time=Timestamp(year=2021, month=12, day=15, hour=10, minute=0),
            duration=30,
            status='',
        )
        
    def test_get(self) -> None:
        request = f'/health_appointment/cancel_appointment/?user_id={self.patient_id}&appointment_id={self.appointment.appointment_id}&Cancel+appointments='
        response = self.client.get(request)
        
        self.assertEqual(
            response.status_code,
            302
        )