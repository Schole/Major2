import uuid
from typing import List

import django.utils.timezone as timezone

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from pandas import Timestamp


class Appointment(models.Model):
    appointment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    doctor_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)
    patient_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)
    create_time = models.DateTimeField(blank=True, null=True,default=timezone.now)
    begin_time = models.DateTimeField(blank=True, null=True,default=timezone.now)

    status = models.CharField(max_length=50)

    duration = models.IntegerField(
        default=30,
        validators=[MaxValueValidator(1440), MinValueValidator(0)]
    )
    """ the time for one appointment section in minutes, can be reset in config.py"""

    def change_appointment_status(self, status):
        self._status = status
        return


def get_appointments(appointment_ids: List[uuid.UUID]) -> List[Appointment]:
    return [
        get_appointment(appointment_id) for appointment_id in appointment_ids
    ]

def get_appointment(appointment_id) -> Appointment:
    objects = Appointment.objects.filter(
        appointment_id__exact=appointment_id
    )
    
    if len(objects) == 0:
        raise ValueError(f"Cannot find doctor with the appointment id {appointment_id}!")
    
    return objects[0]


def create_appointment(
    appointment_id: uuid.UUID,
    doctor_id: uuid.UUID,
    patient_id: uuid.UUID,
    create_time: Timestamp,
    begin_time: Timestamp,
    status: str,
    duration: int,
) -> Appointment:
    return Appointment.objects.create(
        appointment_id=appointment_id,
        doctor_id=doctor_id,
        patient_id=patient_id,
        create_time=create_time,
        begin_time=begin_time,
        status=status,
        duration=duration,
    )