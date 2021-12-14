import uuid
from typing import List

from django.http import HttpResponse
from django.views.generic import DetailView
from django.db.models.query import QuerySet
from django.db.models import Q

from ..models.model_illness import Illness, IllnessCategory
from ..models.model_specialty import Specialty, SpecialtyCategory
from ..models.model_user import Doctor

from .util import send_http_request
from ..util.appointment_helper import find_doctor_available_time, gather_available_time_slots


class ViewAvailableAppointment(DetailView):
    DEFAULT_TEMPLATE = 'health_appointment/availability.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        illnesses, illness_category = ViewAvailableAppointment.get_illness_and_illness_category(request)
        illness_category = int(illness_category)
        illnesses = int(illness_category)
        doctors = self.find_doctors(illness_category)
        user_id = uuid.UUID('250f571986a045618d2449bc66ad39e8')

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
            ViewAvailableAppointment.DEFAULT_TEMPLATE,
        )

    @staticmethod
    def get_illness_and_illness_category(request) -> List[str]:
        return [
            request.GET.get('illness'),
            request.GET.get('category'),
        ]

    @staticmethod
    def find_doctors(category) -> QuerySet:
        specialty_category_id = ViewAvailableAppointment.find_specialty_category(category)
        specialty_category = SpecialtyCategory.objects.filter(
            Q(specialty_category_id__exact=specialty_category_id)
        )
        if len(specialty_category) == 0:
            return specialty_category

        specialty_category = specialty_category[0]
        specialties_ids = specialty_category.specialties

        specialties_ids = SpecialtyCategory.get_illness_category(specialties_ids)

        specialty_models = Specialty.objects.filter(
            Q(specialty_id__in=specialties_ids)
        )
        specialty_ids = [specialty_model.specialty_id for specialty_model in specialty_models]
        doctors = Doctor.objects.filter(
            Q(
                specialty__in=specialty_ids
            )
        )
        return doctors

    @staticmethod
    def find_specialty_category(category) -> int:
        illness_category = IllnessCategory.objects.filter(
            Q(illness_category_id__exact=category)
        )
        if len(illness_category) != 1:
            raise ValueError(f"Cannot find illness category for category {category}!")

        illness_category = illness_category[0]

        specialty_category = illness_category.specialty_category
        return specialty_category

