from health_appointment.models.doctor_model import create_doctor
from health_appointment.models.patient_model import create_patient
from health_appointment.models.illness_model import (
    create_illnesses,
    create_illness_category,
)
from django.contrib.auth.models import User
from health_appointment.models.specialty_model import (
    create_specialty,
    create_specialty_category,
)


def create_user() -> None:
    User.objects.create_user(username='patient_1', password='123')
    User.objects.create_user(username='patient_2', password='123')
    User.objects.create_user(username='patient_3', password='123')
    User.objects.create_user(username='doctor_1', password='123')


def create_system() -> None:
    create_illnesses()
    create_illness_category()
    create_specialty()
    create_specialty_category()
    create_doctor()
    create_patient()