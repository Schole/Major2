import uuid
from django.http import HttpResponse
from django.views.generic import DetailView
from django.shortcuts import redirect

from health_appointment.models.appointment_model import (
   
    get_appointment,
)

from health_appointment.util.appointment_helper import (
    cancel_appointment
)


class CancelAppointmentView(DetailView):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        appointment_id = uuid.UUID(
            request.GET.get(
                "appointment_id"
            )
        )
        
        user_id = uuid.UUID(
            request.GET.get(
                "user_id"
            )
        )

        appointment = get_appointment(appointment_id)

        cancel_appointment(appointment)

        return redirect('/health_appointment/patient_home/' + str(user_id))