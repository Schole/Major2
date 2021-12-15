from typing import List

from pandas import Timestamp

from django.db.models import Q
from django.db.models.query import QuerySet

from health_appointment.models.specialty_model import Specialty, SpecialtyCategory

from health_appointment.models.doctor_model import Doctor
from health_appointment.models.appointment_model import get_appointments, Appointment
from health_appointment.util.appointment_helper import (
    parse_appointment_ids,
    is_appointment_match_time_slots,
)

from health_appointment.util.speciaty_helper import find_specialty_category


def is_doctor_available(
    doctor: Doctor,
    time_slots: List[Timestamp]
) -> bool:
    """Check if a doctor is available at a given time slot."""
    if doctor.empty_appointment():
        return True
    
    appointment_ids = parse_appointment_ids(doctor.active_appointment_ids)
    appointments = get_appointments(appointment_ids)
    
    for appointment in appointments:
        if is_appointment_match_time_slots(
            appointment,
            time_slots,
        ) or appointment.begin_time < time_slots[0] < Appointment.get_end_time(appointment) \
            or appointment.begin_time < time_slots[1] < Appointment.get_end_time(appointment) \
            or time_slots[0] < appointment.begin_time < time_slots[1] \
            or time_slots[0] < Appointment.get_end_time(appointment) < time_slots[1]:
            return False
    
    return True


def find_doctors_available_at_timeslot(
    time_slots: List[Timestamp]
) -> List[Doctor]:
    """
    Find the doctors who are available at a given time slot.
    :param time_slots:
    :return: List[Doctor]
    """
    available_doctors = []
    doctors = Doctor.objects.all()
    for doctor in doctors:
        if is_doctor_available(
            doctor,
            time_slots,
        ):
            available_doctors.append(doctor)
    
    return available_doctors


def find_doctors_with_illness_category(specialty_category: int) -> QuerySet:
    """
    Given a illness category, it finds all the doctors who support it.
    :param specialty_category:
    :return:
    """
    specialty_category_id = find_specialty_category(specialty_category)
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
