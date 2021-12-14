from django.test import TestCase
from pandas import Timestamp
import uuid


from health_appointment.util.appointment_helper import (
    find_available_time_slots,
    get_occupied_offsite_time_slots,
    add_appointment,
    find_doctor_available_time,
    parse_appointment_ids,
    convert_time_slots_to_str,
    convert_time_str_to_timestamp,
    find_time_slot_duration,
)

from health_appointment.models.model_user import Doctor
from health_appointment.models.model_appointment import Appointment

from health_appointment.config.config import Config


class TestAppointmentHelper(TestCase):
    def test_find_available_time_slots(self) -> None:
        available_time_slots = find_available_time_slots(
            occupied_times=[
                [
                    Timestamp(year=2021, month=12, day=15, hour=10, minute=0),
                    Timestamp(year=2021, month=12, day=15, hour=10, minute=30),
                ],
                [
                    Timestamp(year=2021, month=12, day=15, hour=11, minute=0),
                    Timestamp(year=2021, month=12, day=15, hour=11, minute=30),
                ],
                [
                    Timestamp(year=2021, month=12, day=15, hour=12, minute=0),
                    Timestamp(year=2021, month=12, day=15, hour=12, minute=30),
                ],
            ],
            current_time=Timestamp(year=2021, month=12, day=15, hour=10, minute=0),
            min_ahead_showing_availability=1 * 3 * 60,
            time_unit=30,
        )

        self.assertEqual(
            available_time_slots,
            [
                (
                    Timestamp(year=2021, month=12, day=15, hour=10, minute=30),
                    Timestamp(year=2021, month=12, day=15, hour=11, minute=0),
                ),
                (
                    Timestamp(year=2021, month=12, day=15, hour=11, minute=30),
                    Timestamp(year=2021, month=12, day=15, hour=12, minute=00),
                ),
                (
                    Timestamp(year=2021, month=12, day=15, hour=12, minute=30),
                    Timestamp(year=2021, month=12, day=15, hour=13, minute=0),
                )
            ]
        )

    def test_occupied_offsite_time_slots(self) -> None:
        occupied_time_slots = get_occupied_offsite_time_slots(
            Timestamp(year=2021, month=12, day=15),
            hour_start_work=8,
            hour_end_work=17,
        )

        self.assertEqual(
            occupied_time_slots,
            [
                (
                    Timestamp(year=2021, month=12, day=15, hour=0, minute=0),
                    Timestamp(year=2021, month=12, day=15, hour=8, minute=0),
                ),
                (
                    Timestamp(year=2021, month=12, day=15, hour=17, minute=0),
                    Timestamp(year=2021, month=12, day=16, hour=0, minute=0),
                )
            ]
        )

    def test_add_appointment(self) -> None:
        doctor = Doctor.objects.create(
            user_id=uuid.uuid4(),
            contact="doctor_1",
            bio_gender=True,
            type="doctor",
            specialty=1,
            valid_appointment_record=''
        )

        appointment = Appointment.objects.create(
            appointment_id=uuid.uuid4(),
            doctor_id=doctor.user_id,
            patient_id=uuid.uuid4(),
            create_time=Timestamp.now(),
            begin_time=Timestamp.now(),
            duration=10,
            status='',
        )

        add_appointment(
            doctor,
            appointment.appointment_id,
        )

        self.assertEqual(
            doctor.valid_appointment_record,
            str(appointment.appointment_id)
        )

    def test_parse_appointment_ids_single(self) -> None:
        uuid_1 = uuid.uuid4()
        uuids_str = str(uuid_1) + ","
        parsed_uuids = parse_appointment_ids(uuids_str)
        self.assertEqual(
            parsed_uuids[0],
            uuid_1
        )

    def test_parse_appointment_ids(self) -> None:
        uuid_1 = uuid.uuid4()
        uuid_2 = uuid.uuid4()
        uuids = [
            uuid_1,
            uuid_2,
        ]
        uuids_str = ','.join(
            [
                str(x) for x in uuids
            ]
        )

        parsed_uuids = parse_appointment_ids(uuids_str)
        self.assertListEqual(
            parsed_uuids,
            uuids
        )

    def test_find_doctor_available_time(self) -> None:
        doctor = Doctor.objects.create(
            user_id=uuid.uuid4(),
            contact="doctor_1",
            bio_gender=True,
            type="doctor",
            specialty=1,
            valid_appointment_record=''
        )

        appointment_0 = Appointment.objects.create(
            appointment_id=uuid.uuid4(),
            doctor_id=doctor.user_id,
            patient_id=uuid.uuid4(),
            create_time=Timestamp(year=2021, month=12, day=15, hour=10, minute=0),
            begin_time=Timestamp(year=2021, month=12, day=15, hour=10, minute=0),
            duration=30,
            status='',
        )

        appointment_1 = Appointment.objects.create(
            appointment_id=uuid.uuid4(),
            doctor_id=doctor.user_id,
            patient_id=uuid.uuid4(),
            create_time=Timestamp(year=2021, month=12, day=15, hour=11, minute=0),
            begin_time=Timestamp(year=2021, month=12, day=15, hour=11, minute=0),
            duration=30,
            status='',
        )

        add_appointment(
            doctor,
            appointment_0.appointment_id,
        )

        add_appointment(
            doctor,
            appointment_1.appointment_id,
        )

        config = Config()
        config.min_ahead_showing_availability = 24 * 60

        available_time_slots = find_doctor_available_time(
            doctor=doctor,
            config=config,
            today_time=Timestamp(year=2021, month=12, day=15, hour=0, minute=0),
        )

        self.assertListEqual(
            available_time_slots,
            [(Timestamp('2021-12-15 08:00:00'), Timestamp('2021-12-15 08:30:00')),
             (Timestamp('2021-12-15 08:30:00'), Timestamp('2021-12-15 09:00:00')),
             (Timestamp('2021-12-15 09:00:00'), Timestamp('2021-12-15 09:30:00')),
             (Timestamp('2021-12-15 09:30:00'), Timestamp('2021-12-15 10:00:00')),
             (Timestamp('2021-12-15 10:30:00'), Timestamp('2021-12-15 11:00:00')),
             (Timestamp('2021-12-15 11:30:00'), Timestamp('2021-12-15 12:00:00')),
             (Timestamp('2021-12-15 12:00:00'), Timestamp('2021-12-15 12:30:00')),
             (Timestamp('2021-12-15 12:30:00'), Timestamp('2021-12-15 13:00:00')),
             (Timestamp('2021-12-15 13:00:00'), Timestamp('2021-12-15 13:30:00')),
             (Timestamp('2021-12-15 13:30:00'), Timestamp('2021-12-15 14:00:00')),
             (Timestamp('2021-12-15 14:00:00'), Timestamp('2021-12-15 14:30:00')),
             (Timestamp('2021-12-15 14:30:00'), Timestamp('2021-12-15 15:00:00')),
             (Timestamp('2021-12-15 15:00:00'), Timestamp('2021-12-15 15:30:00')),
             (Timestamp('2021-12-15 15:30:00'), Timestamp('2021-12-15 16:00:00')),
             (Timestamp('2021-12-15 16:00:00'), Timestamp('2021-12-15 16:30:00')),
             (Timestamp('2021-12-15 16:30:00'), Timestamp('2021-12-15 17:00:00'))]
        )

    def test_convert_time_slots_to_str(self) -> None:
        time_slots = [Timestamp('2021-12-15 08:00:00'), Timestamp('2021-12-15 08:30:00')]
        time_slots_str = convert_time_slots_to_str(time_slots)
        self.assertEqual(
            time_slots_str,
            "21-12-15-08-00,21-12-15-08-30"
        )

    def test_convert_time_str_to_timestamp(self) -> None:
        time_slots_str = "21-12-15-08-00,21-12-15-08-30"
        time_slots = convert_time_str_to_timestamp(time_slots_str)
        self.assertListEqual(
            time_slots,
            [
                Timestamp('2021-12-15 08:00:00'),
                Timestamp('2021-12-15 08:30:00')
            ]
        )
    
    def test_find_time_slot_duration(self) -> None:
        duration = find_time_slot_duration(
            [
                Timestamp('2021-12-15 08:00:00'),
                Timestamp('2021-12-15 08:30:00')
            ]
        )
        
        self.assertEqual(
            duration,
            30
        )




