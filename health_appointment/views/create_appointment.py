import uuid
from typing import List
from django.http import HttpResponse
from django.views.generic import DetailView

from pandas import Timestamp

from ..models.model_user import (
    get_doctor,
    get_patient,
)

from ..models.model_appointment import create_appointment

from ..util.appointment_helper import (
    add_appointment,
    convert_time_str_to_timestamp,
    find_time_slot_duration,
    find_doctor_with_minimal_appointments,
)

from ..util.doctor_helper import find_available_doctors

from .util import send_http_request

class CreateAppointment(DetailView):
    DEFAULT_TEMPLATE = 'health_appointment/create_appointment_success.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        patient_id, doctor_id, appointment_time = CreateAppointment.get_request_attributes(request)
        appointment_time = convert_time_str_to_timestamp(appointment_time)
        
        if doctor_id == 'not_select':
            doctors = find_available_doctors(appointment_time)
            doctor = find_doctor_with_minimal_appointments(doctors)
            doctor_id = doctor.user_id
        else:
            doctor = get_doctor(doctor_id)
            
        patient = get_patient(patient_id)

        duration = find_time_slot_duration(appointment_time)
        
        appointment = create_appointment(
            appointment_id=uuid.uuid4(),
            doctor_id=doctor_id,
            patient_id=patient_id,
            create_time=Timestamp.now(),
            begin_time=appointment_time[0],
            status="active",
            duration=duration,
        )
        
        add_appointment(
            doctor,
            appointment.appointment_id
        )

        add_appointment(
            patient,
            appointment.appointment_id
        )

        return send_http_request(
            request,
            {
                'doctor': doctor,
                'appointment_time':appointment_time[0],
            },
            CreateAppointment.DEFAULT_TEMPLATE,
        )

    @staticmethod
    def get_request_attributes(request) -> List[str]:
        return [
            request.GET.get('user_id'),
            request.GET.get('doctor_id'),
            request.GET.get('appointment_time_slot'),
        ]