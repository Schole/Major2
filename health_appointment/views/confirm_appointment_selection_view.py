from typing import List

from pandas import Timestamp
from django.http import HttpResponse
from django.views.generic import DetailView


from .util import send_http_request
from ..models.illness_model import (
    get_illness_category_name,
    get_illness_name,
)
from ..models.doctor_model import get_doctor


class ConfirmAppointmentView(DetailView):
    DEFAULT_TEMPLATE = 'health_appointment/create_appointment_success.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        appointment_time_slot,doctor_id,illnesses,illness_category = ConfirmAppointmentView.get_request_attributes(request)
        illness_category = int(illness_category)
        illnesses = int(illnesses)

        illnesses_name = get_illness_name(illnesses)
        illness_category_name = get_illness_category_name(illness_category)
        doctor_name = get_doctor(doctor_id).name

        return send_http_request(
            request,
            {
                'doctor_name': doctor_name,
                'appointment_time_slot': appointment_time_slot,
                'illnesses_name': illnesses_name,
                'illness_category_name': illness_category_name,
            },
            ConfirmAppointmentView.DEFAULT_TEMPLATE,
        )

    @staticmethod
    def get_request_attributes(request) -> List[str]:
        return [
            request.GET.get('appointment_time_slot'),
            request.GET.get('doctor_id'),
            request.GET.get('illnesses'),
            request.GET.get('illness_category'),
        ]


