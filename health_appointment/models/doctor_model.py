from __future__ import annotations

import sys
from typing import List, Union
import uuid

from django.db import models

from health_appointment.models.user_model import User


class Doctor(User):
    specialty = models.IntegerField(default=-1)
    active_appointment_ids = models.CharField(default='', max_length=160000)
    """Contains a 'list' of upcoming appointment ids."""
    
    @classmethod
    def get_class(cls) -> User:
        return getattr(sys.modules[__name__], cls.__name__)
    
    @classmethod
    def update_specialty(
        cls,
        doctor: Union[Doctor, uuid.UUID],
        specialty,
    ):
        cls.update_attribute(
            doctor,
            "specialty",
            specialty,
        )
    
    @classmethod
    def update_active_appointment_ids(
        cls,
        doctor: Union[Doctor, uuid.UUID],
        active_appointment_ids,
    ):
        cls.update_attribute(
            doctor,
            "active_appointment_ids",
            active_appointment_ids,
        )
        
    def empty_appointment(self) -> bool:
        return self.active_appointment_ids == ""
    
def get_doctors(doctor_ids: List[uuid.UUID]) -> List[User]:
    return [
        get_doctor(doctor_id) for doctor_id in doctor_ids
    ]

def get_doctor(doctor_id) -> User:
    return Doctor.get_user(doctor_id)

def create_doctor():
    indexes = [1, 2, 3, 4, 5, 6, 7, 8]
    names = [
        "name_1",
        "name_2",
        "name_3",
        "name_4",
        "name_5",
        "name_6",
        "name_7",
        "name_8",
    ]
    contacts = ["Rutgers University"] * 8
    
    bio_genders = [0, 1, 0, 1, 0, 1, 0, 1]
    types = ["doctor", "doctor", "doctor", "doctor", "doctor", "doctor", "doctor", "doctor"]
    specialties = [1, 1, 1, 2, 3, 3, 4, 4]
    for index, name, contact, gender, t, specialty in zip(indexes, names, contacts, bio_genders, types, specialties):
        Doctor.objects.create(
            login_name=name,
            name=name,
            contact=name,
            bio_gender=gender,
            type=t,
            specialty=specialty,
        )