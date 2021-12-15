from health_appointment.views.create_appointment_view import CreateAppointmentView
from unittest.mock import MagicMock, patch
from django.test import TestCase, RequestFactory


class TestCreateAppointmentView(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
    

