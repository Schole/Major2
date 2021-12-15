import uuid
from django.test import TestCase

from health_appointment.models.patient_model import (
    Patient,
    create_patient,
)


class TestPatientModel(TestCase):
    def test_patient_default_setting(self) -> None:
        patient = Patient.objects.create()
        self.assertEqual(
            patient.active_appointment_ids,
            ''
        )
        
        self.assertEqual(
            patient.bio_gender,
            True,
        )
        
        self.assertEqual(
            patient.name,
            '',
        )
        
        self.assertEqual(
            patient.contact,
            '',
        )
        
        self.assertEqual(
            patient.type,
            '',
        )
    
    def test_patient_setting(self) -> None:
        user_id = uuid.uuid4()
        name = "test_name"
        contact = "Rutgers University"
        bio_gender = False
        type = "patient"
        active_appointment_ids = "1234"
        
        patient = Patient.objects.create(
            user_id=user_id,
            name=name,
            contact=contact,
            bio_gender=bio_gender,
            type=type,
            active_appointment_ids=active_appointment_ids
        )
        
        self.assertEqual(
            patient.user_id,
            user_id,
        )
        
        self.assertEqual(
            patient.name,
            name,
        )
        
        self.assertEqual(
            patient.contact,
            contact
        )
        
        self.assertEqual(
            patient.bio_gender,
            bio_gender,
        )
        
        self.assertEqual(
            patient.type,
            type
        )
        
        self.assertEqual(
            patient.active_appointment_ids,
            active_appointment_ids,
        )
    
    def test_get_patient(self) -> None:
        patient_0 = Patient.objects.create()
        patient_1 = Patient.objects.create()
        
        patients = Patient.get_users(
            [
                patient_0.user_id,
                patient_1.user_id,
            ]
        )
        
        self.assertListEqual(
            patients,
            [
                patient_0,
                patient_1,
            ]
        )
    
    def test_create_patient(self) -> None:
        create_patient()