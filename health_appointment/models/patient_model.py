from __future__ import annotations

import sys
import uuid

from typing import Union
from django.db import models

from health_appointment.models.user_model import User


class Patient(User):
    active_appointment_ids = models.CharField(default='', max_length=1600)
    """valid_appointment_record; CharField, contains a 'list' of upcoming appointment ids."""

    @classmethod
    def get_class(cls) -> User:
        return getattr(sys.modules[__name__], cls.__name__)

    @classmethod
    def update_active_appointment_ids(
        cls,
        patient: Union[Patient, uuid.UUID],
        active_appointment_ids,
    ):
        cls.update_attribute(
            patient,
            "active_appointment_ids",
            active_appointment_ids,
        )
        
def create_patient():
    patient_num = 8
    indexes = [uuid.uuid4() for _ in range(patient_num)]
    
    names = [
        "patient_1",
        "patient_2",
        "patient_3",
        "patient_4",
        "patient_5",
        "patient_6",
        "patient_7",
        "patient_8",
    ]
    contacts = ["Rutgers University"] * 8
    bio_genders = [0, 1, 0, 1, 0, 1, 0, 1]
    
    types = ["patient"] * patient_num
    
    for index, name, contact, gender, t in zip(indexes, names, contacts, bio_genders, types):
        Patient.objects.create(
            user_id=index,
            login_name=name,
            name=name,
            contact=name,
            bio_gender=gender,
            type=t,
        )
