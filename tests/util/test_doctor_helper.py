import uuid

from django.test import TestCase

from pandas import Timestamp

from health_appointment.util.doctor_helper import (
    find_doctors_with_illness_category,
    find_doctors_available_at_timeslot,
    is_doctor_available,
)

from health_appointment.util.appointment_helper import add_appointment

from health_appointment.models.doctor_model import (
    Doctor,
    create_doctor,
)
from health_appointment.models.appointment_model import (
    create_appointment,
)
from health_appointment.models.illness_model import (
    IllnessCategory,
)
from health_appointment.models.specialty_model import (
    SpecialtyCategory,
    Specialty,
)


class TestAppointmentHelper(TestCase):
    def test_is_doctor_available(self) -> None:
        doctor = Doctor.objects.create()
        
        appointment = create_appointment(
            doctor_id=doctor.user_id,
            patient_id=uuid.uuid4(),
            create_time=Timestamp(year=2021, month=12, day=15, hour=10, minute=0),
            begin_time=Timestamp(year=2021, month=12, day=15, hour=10, minute=0),
            duration=10,
            status="active",
        )

        add_appointment(
            doctor,
            appointment.appointment_id
        )
        
        self.assertFalse(
            is_doctor_available(
                doctor,
                [
                    Timestamp(year=2021, month=12, day=15, hour=10, minute=0),
                    Timestamp(year=2021, month=12, day=15, hour=10, minute=30),
                ]
            )
        )

        self.assertTrue(
            is_doctor_available(
                doctor,
                [
                    Timestamp(year=2021, month=12, day=15, hour=11, minute=0),
                    Timestamp(year=2021, month=12, day=15, hour=11, minute=30),
                ]
            )
        )
    
    def test_find_doctors_with_illness_category(self) -> None:
        doctor = Doctor.objects.create(
            specialty=1
        )
        doctor_1 = Doctor.objects.create(
            specialty=2
        )

        IllnessCategory.objects.create(
            illness_category_id=1
        )
        SpecialtyCategory.objects.create(
            specialties='1'
        )
        Specialty.objects.create(
            specialty_id=1
        )
        doctors = find_doctors_with_illness_category(1)
        
        self.assertEqual(
            doctors[0],
            doctor
        )
    
    def test_find_doctors_available_at_timeslot(self) -> None:
        doctor = Doctor.objects.create()
        doctor_1 = Doctor.objects.create()
        
        appointment = create_appointment(
            doctor_id=doctor.user_id,
            patient_id=uuid.uuid4(),
            create_time=Timestamp(year=2021, month=12, day=15, hour=10, minute=0),
            begin_time=Timestamp(year=2021, month=12, day=15, hour=10, minute=0),
            duration=10,
            status="active",
        )
    
        add_appointment(
            doctor,
            appointment.appointment_id
        )
        
        doctors = find_doctors_available_at_timeslot(
            [
                Timestamp(year=2021, month=12, day=15, hour=10, minute=0),
                Timestamp(year=2021, month=12, day=15, hour=10, minute=10)
            ]
        )
        
        self.assertListEqual(
            doctors,
            [
                doctor_1
            ]
        )

        doctors_1 = find_doctors_available_at_timeslot(
            [
                Timestamp(year=2021, month=12, day=15, hour=11, minute=0),
                Timestamp(year=2021, month=12, day=15, hour=11, minute=10)
            ]
        )

        self.assertListEqual(
            doctors_1,
            [
                doctor,
                doctor_1
            ]
        )
        
    def test_create_doctor(self) -> None:
        create_doctor()