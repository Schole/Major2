import uuid

from typing import List, Union

from pandas import Timestamp, Timedelta, to_datetime
from django.db.models import Q

from health_appointment.models.user_model import User
from health_appointment.models.doctor_model import (
    Doctor,
)
from health_appointment.models.patient_model import Patient
from health_appointment.models.appointment_model import (
    Appointment,
    get_appointment,
)
from health_appointment.util.user_helper import convert_user
from health_appointment.config.config import Config


def find_doctor_with_minimal_appointments(
    doctors: List[Doctor],
) -> Doctor:
    """
    Use a greedy algorithm to assign a doctor with minimal appointments.
    :param doctors:
    :return:
    """
    dict_doctor_to_upcoming_appointments = dict()
    
    for doctor in doctors:
        active_appointments = parse_appointment_ids(doctor.active_appointment_ids)
        number_of_active_appointments = len(active_appointments)
        dict_doctor_to_upcoming_appointments[doctor] = number_of_active_appointments
    
    best_doctor = min(dict_doctor_to_upcoming_appointments, key=dict_doctor_to_upcoming_appointments.get)
    return best_doctor


def add_appointment(
    user: Union[Doctor, Patient],
    appointment: uuid,
) -> None:
    """
    Add an appointment to a doctor or a patient.
    :param user:
    :param appointment:
    :return:
    """
    appointment_str = str(appointment)
    current_appointments = user.active_appointment_ids
    if current_appointments == "":
        user.active_appointment_ids = appointment_str + ","
    else:
        user.active_appointment_ids = current_appointments + "," + appointment_str
    
    user.save()
    
    return None


def cancel_appointments(
    appointments: List[
        Union[
            uuid.UUID, Appointment,
        ]
    ]
):
    for appointment in appointments:
        cancel_appointment(appointment)


def cancel_appointment(
    appointment: Union[uuid.UUID, Appointment],
):
    if isinstance(
        appointment,
        uuid.UUID
    ):
        appointment = get_appointment(appointment)
    
    doctor_id = appointment.doctor_id
    patient_id = appointment.patient_id
    
    delete_appointment_from_user(
        appointment_id=appointment.appointment_id,
        user_id=doctor_id
    )
    
    delete_appointment_from_user(
        appointment_id=appointment.appointment_id,
        user_id=patient_id
    )


def delete_appointment_from_user(
    appointment_id: Union[uuid.UUID, str],
    user_id: uuid.UUID,
):
    user = convert_user(user_id)
    active_appointment_ids = user.active_appointment_ids
    active_appointments = set(parse_appointment_ids(active_appointment_ids))
    
    if isinstance(
        appointment_id,
        str
    ):
        appointment_id = uuid.UUID(appointment_id)
        
    if appointment_id not in active_appointments:
        return None
    
    active_appointments.remove(appointment_id)
    
    if len(active_appointments) == 0:
        active_appointment_ids = ''
    else:
        active_appointment_ids = ','.join(
            [
                str(active_appointment_id) for active_appointment_id in active_appointments
            ]
        )
    
    user.update_active_appointment_ids(
        user,
        active_appointment_ids,
    )


def parse_appointment_ids(
    appointment_ids: str,
) -> List[uuid.UUID]:
    return [
        uuid.UUID(
            uid
        ) for uid in appointment_ids.split(',') if uid != ""
    ]


def find_doctor_available_time(
    doctor: Doctor,
    config: Config = Config(),
    today_time=to_datetime("today").normalize(),
):
    """
    Find the available time of the doctor.
    :param doctor:
    :param config
    :param today_time
    :return:
    """
    appointment_records = doctor.active_appointment_ids
    appointment_ids = parse_appointment_ids(appointment_records)
    
    occupied_times = get_occupied_offsite_time_slots(
        today_time,
        config.doctor_work_start_hour,
        config.doctor_work_end_hour,
    )
    
    for record_id in appointment_ids:
        appointment = Appointment.objects.filter(
            Q(appointment_id__exact=record_id)
        )
        if len(appointment) != 1:
            raise ValueError("Failed to find the appointment!")
        
        appointment = appointment[0]
        
        start_time = appointment.begin_time
        duration = appointment.duration
        end_time = start_time + Timedelta(duration, unit="min")
        
        occupied_times.append(
            (
                start_time,
                end_time,
            )
        )
    
    available_time_slots = find_available_time_slots(
        occupied_times,
        today_time,
        config.min_ahead_showing_availability,
        config.time_unit,
    )
    
    return available_time_slots


def find_available_time_slots(
    occupied_times: List[List[Timestamp,]],
    current_time: Timestamp,
    minutes_ahead_showing_availability: int,
    time_unit: int,
):
    """Given the current time, time window, time unit and occupied time,
    this function finds the available time slots in the window.
    :param occupied_times:
    :param current_time
    :param minutes_ahead_showing_availability
    :param time_unit
    """
    available_time_slots = []
    
    total_unit_numbers = int(minutes_ahead_showing_availability / time_unit)
    
    for unit in range(total_unit_numbers):
        start_time = current_time + Timedelta(unit * time_unit, unit="min")
        end_time = current_time + Timedelta(unit * time_unit + time_unit, unit="min")
        
        # TODO: optimize O(N^2) to O(N)
        occupied = False
        for start_occupied_time, end_occupied_time in occupied_times:
            if (start_occupied_time < start_time < end_occupied_time) or (
                start_occupied_time < end_time < end_occupied_time) or (
                start_occupied_time == start_time and end_occupied_time == end_time):
                occupied = True
                break
        
        if not occupied:
            available_time_slots.append(
                (
                    start_time,
                    end_time,
                )
            )
    
    return available_time_slots


def gather_available_time_slots(
    available_time_slots_for_all_doctors: dict,
) -> dict:
    """Given a list of lists of available time slots for all the appropriate doctors,
        gather the same time slots and return the time slots and the number of
        its copies.
        :param available_time_slots_for_all_doctors:
    """
    dict_time_slots_to_doctor_ids = dict()
    
    for doctor_id, available_time_slots in available_time_slots_for_all_doctors.items():
        doctor = Doctor.get_user(doctor_id)
        for time_slot in available_time_slots:
            time_slot = convert_time_slots_to_str(time_slot)
            if time_slot in dict_time_slots_to_doctor_ids:
                dict_time_slots_to_doctor_ids[
                    time_slot
                ].append([doctor_id, doctor.name])
            else:
                dict_time_slots_to_doctor_ids[
                    time_slot
                ] = [[doctor_id, doctor.name]]
    
    return dict(sorted(dict_time_slots_to_doctor_ids.items()))


def convert_time_slots_to_str(
    time_slots: List[Timestamp]
) -> str:
    return ','.join(
        [
            time_slot.strftime("%y-%m-%d-%H-%M") for time_slot in time_slots
        ]
    )


def convert_time_str_to_timestamp(time_slots: str) -> List[Timestamp]:
    return [
        to_datetime(time_slot, format="%y-%m-%d-%H-%M") for time_slot in time_slots.split(',')
    ]


def find_time_slot_duration(time_slots: List[Timestamp]) -> int:
    diff = time_slots[1] - time_slots[0]
    return diff.seconds // 60


def get_occupied_offsite_time_slots(
    today: Timestamp,
    hour_start_work: int,
    hour_end_work: int,
):
    """
    Block the time slots that beyond office hours.
    :param today: current time
    :param hour_start_work: the hour to start work, e.g., 8am
    :param hour_end_work: the hour to end work, e.g., 17 pm
    :return:
    """
    occupied_time_slots = [
        (
            today,
            today + Timedelta(
                hour_start_work,
                unit="hour",
            )
        ),
        (
            today + Timedelta(
                hour_end_work,
                unit="hour",
            ),
            today + Timedelta(
                24, unit="hours",
            )
        )
    ]
    
    return occupied_time_slots


def is_appointment_match_time_slots(
    appointment: Appointment,
    time_slots: List[Timestamp],
) -> bool:
    return appointment.begin_time == time_slots[0] and (
        appointment.begin_time + Timedelta(appointment.duration, unit='min')) == time_slots[1]
