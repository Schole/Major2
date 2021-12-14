from typing import List
import uuid

from django.db import models
from pandas import Timestamp


class User(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    contact = models.CharField(max_length=50, default='')
    bio_gender = models.BooleanField(default=True)
    
    type = models.CharField(max_length=50, default='')
    
    def is_quality_register(self) -> bool:
        """bool; check if the user is qualified for appointment registration
        this can be done based on the type attribute."""


class Patient(User):
    valid_appointment_record = models.CharField(default='', max_length=1600)
    """valid_appointment_record; CharField, contains a 'list' of upcoming appointment ids."""


class Doctor(User):
    specialty = models.IntegerField(default=-1)
    valid_appointment_record = models.CharField(default='', max_length=160000)
    """valid_appointment_record; CharField, contains a 'list' of upcoming appointment ids."""


def get_doctors(doctor_ids: List[uuid.UUID]) -> List[Doctor]:
    return [
        get_doctor(doctor_id) for doctor_id in doctor_ids
    ]

def get_doctor(doctor_id) -> Doctor:
    objects = Doctor.objects.filter(
        user_id__exact=doctor_id
    )
    
    if len(objects) == 0:
        raise ValueError(f"Cannot find doctor with the doctor id {doctor_id}!")
    
    return objects[0]


def get_patient(patient_id) -> Patient:
    objects = Patient.objects.filter(
        user_id__exact=patient_id
    )
    
    if len(objects) == 0:
        raise ValueError(f"Cannot find doctor with the patient id {patient_id}!")
    
    return objects[0]


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
    bio_genders = [0, 1, 0, 1, 0, 1, 0, 1]
    types = ["doctor", "doctor", "doctor", "doctor", "doctor", "doctor", "doctor", "doctor"]
    specialties = [1, 1, 1, 2, 3, 3, 4, 4]
    for index, name, gender, t, specialty in zip(indexes, names, bio_genders, types, specialties):
        Doctor.objects.create(
            user_id=index,
            contact=name,
            bio_gender=gender,
            type=t,
            specialty=specialty,
        )
    print("created!")
    
    # Bar.objects.all().delete()

def create_patient():
    patient_num = 8
    indexes =[uuid.uuid4() for _ in range(patient_num)]
    
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
    bio_genders = [0, 1, 0, 1, 0, 1, 0, 1]
    
    types = ["patient"] * patient_num
    
    for index, name, gender, t in zip(indexes, names, bio_genders, types):
        Patient.objects.create(
            user_id=index,
            contact=name,
            bio_gender=gender,
            type=t,
        )
    print("created!")
    # Bar.objects.all().delete()
