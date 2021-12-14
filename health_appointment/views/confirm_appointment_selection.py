from typing import List
import uuid

from pandas import Timestamp, Timedelta, to_datetime
from django.http import HttpResponse
from django.views.generic import DetailView
from django.template import loader
from django.db.models.query import QuerySet
from django.db.models import Q

from ..models.model_illness import Illness, IllnessCategory
from ..models.model_specialty import Specialty, SpecialtyCategory
from ..models.model_user import Doctor

from .util import send_http_request
from ..util.appointment_helper import find_doctor_available_time, gather_available_time_slots


class ConfirmAppointment(DetailView):
    DEFAULT_TEMPLATE = 'health_appointment/create_appointment_success.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        appointment_time_slot,doctor_id,illnesses,illness_category = ConfirmAppointment.get_request_attributes(request)
        illness_category = int(illness_category)
        illnesses = int(illnesses)
        appointment_time_slot = List[Timestamp](appointment_time_slot)

        illnesses_name = ConfirmAppointment.get_illness_category_name(illnesses)
        illness_category_name = ConfirmAppointment.get_illness_category_name(illness_category)
        doctor_name = ConfirmAppointment.get_doctor_name(doctor_id)

        return send_http_request(
            request,
            {
                'doctor_name': doctor_name,
                'appointment_time_slot': appointment_time_slot,
                'illnesses_name': illnesses_name,
                'illness_category_name': illness_category_name,
            },
            ConfirmAppointment.DEFAULT_TEMPLATE,
        )

    @staticmethod
    def get_request_attributes(request) -> List[str]:
        return [
            request.GET.get('appointment_time_slot'),
            request.GET.get('doctor_id'),
            request.GET.get('illnesses'),
            request.GET.get('illness_category'),
        ]

    @staticmethod
    def get_illness_category_name(illness_category):
        illness_category_object = IllnessCategory.objects.filter(
            Q(illness_category_id__exact=illness_category)
        )
        if len(illness_category_object) == 0:
            raise ValueError(f"Cannot find illness category for category {illness_category}!")

        return illness_category_object[0].name

    @staticmethod
    def get_illness(illness):
        illness_object = Illness.objects.filter(
            Q(illness_id__exact=illness)
        )
        if len(illness_object) == 0:
            raise ValueError(f"Cannot find illness for illness {illness}!")

        return illness_object[0].name

    @staticmethod
    def get_doctor_name(doctor_id):
        if doctor_id is None:
            return None
        doctor_object = Doctor.objects.filter(
            Q(doctor_id__exact=doctor_id)
        )
        if len(doctor_object) == 0:
            raise ValueError(f"Cannot find doctor for doctor {doctor_id}!")

        return doctor_object[0].name