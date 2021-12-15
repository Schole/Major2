from typing import Union
import uuid

from health_appointment.models.user_model import User
from health_appointment.models.doctor_model import Doctor
from health_appointment.models.patient_model import Patient


def convert_user(
    user_id: uuid.UUID
) -> Union[Doctor, Patient]:
    user = User.get_user(user_id)
    
    if user.type == 'doctor':
        return Doctor.get_user(user_id)
    
    if user.type == 'patient':
        return Patient.get_user(user_id)
    
    raise ValueError(f"Cannot convert user with user_id {user_id}!")