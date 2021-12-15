import uuid
from typing import List

from django.http import HttpResponse
from django.views.generic import DetailView
from .util import send_http_request
from ..util.appointment_helper import find_doctor_available_time, gather_available_time_slots
from ..util.doctor_helper import find_doctors_with_illness_category


class CheckAvailableAppointmentView(DetailView):
    DEFAULT_TEMPLATE = 'health_appointment/create_appointment.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        illnesses, illness_category = CheckAvailableAppointmentView.get_illness_and_illness_category(request)
        illness_category = int(illness_category)
        illnesses = int(illness_category)
        doctors = find_doctors_with_illness_category(illness_category)
    
        user_id = request.GET.get('user_id')

        if len(doctors) == 0:
            return send_http_request(
                request,
                {

                },
                'health_appointment/no_availability.html'
            )

        appointments = {
            doctor.user_id: find_doctor_available_time(
                doctor,
            ) for doctor in doctors
        }

        dict_gathered_appointments = gather_available_time_slots(appointments)

        return send_http_request(
            request,
            {
                'doctors': doctors,
                'user_id': user_id,
                'dict_gathered_appointments': dict_gathered_appointments,
                'illnesses': illnesses,
                'illness_category': illness_category,
            },
            CheckAvailableAppointmentView.DEFAULT_TEMPLATE,
        )

    @staticmethod
    def get_illness_and_illness_category(request) -> List[str]:
        return [
            request.GET.get('illness'),
            request.GET.get('category'),
        ]

