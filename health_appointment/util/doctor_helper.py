from typing import List

from pandas import Timestamp

from ..models.model_user import Doctor
from ..models.model_appointment import get_appointments
from ..util.appointment_helper import (
    parse_appointment_ids,
    is_appointment_match_time_slots,
)


def check_doctor_is_available(
    doctor: Doctor,
    time_slots: List[Timestamp]
) -> bool:
    """Check if a doctor is available at a given time slot."""
    appointment_ids = parse_appointment_ids(doctor.valid_appointment_record)
    appointments = get_appointments(appointment_ids)
    
    for appointment in appointments:
        if is_appointment_match_time_slots(
            appointment,
            time_slots,
        ):
            return False
    
    return True
    
    
def find_available_doctors(time_slots: List[Timestamp]) -> List[Doctor]:
    available_doctors = []
    doctors = Doctor.objects.all()
    for doctor in doctors:
        if check_doctor_is_available(
            doctor,
            time_slots,
        ):
            available_doctors.append(doctor)
    
    return available_doctors