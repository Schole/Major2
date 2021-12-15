from typing import List

from django.http import HttpResponse
from django.views.generic import DetailView
from django.contrib.auth.views import LoginView

from ..models.illness_model import (
    Illness,
    IllnessCategory,
)
from health_appointment.views.util import send_http_request
from health_appointment.models.patient_model import Patient
from health_appointment.models.doctor_model import Doctor
from health_appointment.util.appointment_helper import parse_appointment_ids
from health_appointment.models.appointment_model import get_appointments


class PatientHomeView(DetailView):
    DEFAULT_TEMPLATE = 'health_appointment/patient_home.html'
    
    def get(self, request, *args, **kwargs) -> HttpResponse:
        illness_category = IllnessCategory.objects.all()
        illness = Illness.objects.all()

        user_id = kwargs.get('user_id')
        user = Patient.get_user(user_id)
        
        appointment_ids = parse_appointment_ids(user.active_appointment_ids)
        appointments = get_appointments(appointment_ids)
        doctor_ids = [appointment.doctor_id for appointment in appointments]
        doctors = Doctor.get_users(doctor_ids)
        
        context = {
            'user_id': user_id,
            'illness_categories': illness_category,
            'illnesses': illness,
            "appointments": zip(appointments, doctors),
            #"doctors": doctors
        }
        
        return send_http_request(
            request,
            context,
            self.DEFAULT_TEMPLATE,
        )