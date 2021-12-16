import uuid
from typing import List
from django.http import HttpResponse
from django.views.generic import DetailView
from django.shortcuts import redirect

from pandas import Timestamp

from health_appointment.models.doctor_model import (
    get_doctor,
)
from health_appointment.models.patient_model import (
    Patient
)
from health_appointment.models.appointment_model import create_appointment

from health_appointment.util.appointment_helper import (
    add_appointment,
    convert_time_str_to_timestamp,
    find_time_slot_duration,
    find_doctor_with_minimal_appointments,
)

from health_appointment.util.doctor_helper import find_doctors_available_at_timeslot


class CreateAppointmentView(DetailView):
    DEFAULT_TEMPLATE = 'health_appointment/patient_home.html'
 
    def get(self, request, *args, **kwargs) -> HttpResponse:
        patient_id, doctor_id, appointment_time = CreateAppointmentView.get_request_attributes(request)
        appointment_time = convert_time_str_to_timestamp(appointment_time)
        
        if doctor_id == 'not_select':
            doctors = find_doctors_available_at_timeslot(appointment_time)
            doctor = find_doctor_with_minimal_appointments(doctors)
            doctor_id = doctor.user_id
        else:
            doctor = get_doctor(uuid.UUID(doctor_id))
            
        patient = Patient.get_user(uuid.UUID(patient_id))

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

        # from health_appointment.views.util import send_http_request
        #
        # return send_http_request(
        #     request,
        #     {
        #         "doctor": doctor,
        #         "appointment_time": appointment.begin_time
        #     },
        #     'health_appointment/create_appointment_success.html'
        # )
        return redirect('/health_appointment/patient_home/'+str(patient.user_id))

    @staticmethod
    def get_request_attributes(request) -> List[str]:
        return [
            request.GET.get('user_id'),
            request.GET.get('doctor_id'),
            request.GET.get('appointment_time_slot'),
        ]