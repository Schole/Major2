import uuid

from django.test import TestCase

from health_appointment.models.doctor_model import (
    Doctor,
    get_doctors,
)


class TestDoctorModel(TestCase):
    def test_doctor_default_setting(self) -> None:
        doctor = Doctor.objects.create()
        self.assertEqual(
            doctor.active_appointment_ids,
            ''
        )
        
        self.assertEqual(
            doctor.bio_gender,
            True,
        )
        
        self.assertEqual(
            doctor.name,
            '',
        )
        
        self.assertEqual(
            doctor.contact,
            '',
        )
        
        self.assertEqual(
            doctor.type,
            '',
        )
    
    def test_doctor_setting(self) -> None:
        user_id = uuid.uuid4()
        name = "test_name"
        contact = "Rutgers University"
        bio_gender = False
        type = "doctor"
        specialty = 123
        active_appointment_ids = "1234"
        
        doctor = Doctor.objects.create(
            user_id=user_id,
            name=name,
            contact=contact,
            bio_gender=bio_gender,
            type=type,
            specialty=specialty,
            active_appointment_ids=active_appointment_ids
        )
        
        self.assertEqual(
            doctor.user_id,
            user_id,
        )
        
        self.assertEqual(
            doctor.name,
            name,
        )
        
        self.assertEqual(
            doctor.contact,
            contact
        )
        
        self.assertEqual(
            doctor.bio_gender,
            bio_gender,
        )
        
        self.assertEqual(
            doctor.type,
            type
        )
        
        self.assertEqual(
            doctor.specialty,
            specialty
        )
        
        self.assertEqual(
            doctor.active_appointment_ids,
            active_appointment_ids,
        )
    
    def test_get_doctors(self) -> None:
        doctor_0 = Doctor.objects.create()
        doctor_1 = Doctor.objects.create()
        
        doctors = get_doctors(
            [
                doctor_0.user_id,
                doctor_1.user_id,
            ]
        )
        
        self.assertListEqual(
            doctors,
            [
                doctor_0,
                doctor_1,
            ]
        )

    def test_update_name(self) -> None:
        doctor = Doctor.objects.create()
        Doctor.update_name(
            doctor,
            "updated_name"
        ),
        
        self.assertEqual(
            doctor.name,
            "updated_name",
        )

    def test_update_specialty(self) -> None:
        doctor = Doctor.objects.create()
        Doctor.update_specialty(
            doctor,
            123
        ),
    
        self.assertEqual(
            doctor.specialty,
            123
        )