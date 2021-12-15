import uuid
from django.test import TestCase
from pandas import Timestamp

from health_appointment.models.appointment_model import (
    Appointment,
    get_appointments,
    create_appointment,
)


class TestAppointmentModel(TestCase):
    def test_appointment_setting(self) -> None:
        appointment_id = uuid.uuid4()
        doctor_id = uuid.uuid4()
        patient_id = uuid.uuid4()
        create_time = Timestamp(year=2021, month=12, day=15, hour=10, minute=0)
        begin_time = Timestamp(year=2021, month=12, day=15, hour=10, minute=0)
        duration = 10
        
        appointment = Appointment.objects.create(
            appointment_id=appointment_id,
            doctor_id=doctor_id,
            patient_id=patient_id,
            create_time=create_time,
            begin_time=begin_time,
            duration=duration,
            status='',
        )
        
        self.assertEqual(
            appointment.appointment_id,
            appointment_id,
        )
        
        self.assertEqual(
            appointment.doctor_id,
            doctor_id,
        )
        
        self.assertEqual(
            appointment.patient_id,
            patient_id,
        )
        
        self.assertEqual(
            appointment.create_time,
            create_time,
        )
        
        self.assertEqual(
            appointment.begin_time,
            begin_time,
        )
        
        self.assertEqual(
            appointment.duration,
            duration
        )
        
        self.assertEqual(
            appointment.status,
            ''
        )
    
    def test_get_appointments(self):
        appointment_0 = Appointment.objects.create(
            appointment_id=uuid.uuid4(),
            doctor_id=uuid.uuid4(),
            patient_id=uuid.uuid4(),
            create_time=Timestamp(year=2021, month=12, day=15, hour=10, minute=0),
            begin_time=Timestamp(year=2021, month=12, day=15, hour=10, minute=0),
            duration=10,
            status='',
        )
        
        appointment_1 = Appointment.objects.create(
            appointment_id=uuid.uuid4(),
            doctor_id=uuid.uuid4(),
            patient_id=uuid.uuid4(),
            create_time=Timestamp(year=2021, month=12, day=15, hour=10, minute=0),
            begin_time=Timestamp(year=2021, month=12, day=15, hour=10, minute=0),
            duration=10,
            status='',
        )
        
        appointments = get_appointments(
            [
                appointment_0.appointment_id, appointment_1.appointment_id
            ]
        )
        
        self.assertListEqual(
            appointments,
            [
                appointment_0,
                appointment_1,
            ]
        )
    
    def test_create_appointment(self) -> None:
        appointment_id = uuid.uuid4()
        doctor_id = uuid.uuid4()
        patient_id = uuid.uuid4()
        create_time = Timestamp(year=2021, month=12, day=15, hour=10, minute=0)
        begin_time = Timestamp(year=2021, month=12, day=15, hour=10, minute=0)
        duration = 10
        status = 'active'
        
        appointment = create_appointment(
            appointment_id=appointment_id,
            doctor_id=doctor_id,
            patient_id=patient_id,
            create_time=create_time,
            begin_time=begin_time,
            duration=duration,
            status=status,
        )
        
        self.assertEqual(
            appointment.appointment_id,
            appointment_id,
        )
        
        self.assertEqual(
            appointment.doctor_id,
            doctor_id,
        )
        
        self.assertEqual(
            appointment.patient_id,
            patient_id,
        )
        
        self.assertEqual(
            appointment.create_time,
            create_time,
        )
        
        self.assertEqual(
            appointment.begin_time,
            begin_time,
        )
        
        self.assertEqual(
            appointment.duration,
            duration
        )
        
        self.assertEqual(
            appointment.status,
            status
        )
