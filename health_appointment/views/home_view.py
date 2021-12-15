from django.views.generic import DetailView
from django.shortcuts import redirect

from health_appointment.models.user_model import User
from health_appointment.models.doctor_model import Doctor
from health_appointment.models.patient_model import Patient


class HomeView(DetailView):
    def get(self, request, *args, **kwargs):
        login_name = request.user.get_username()
        user = User.get_user(login_name)
        
        if user.type == "doctor":
            user = Doctor.get_user(login_name)
            # TODO: add doctor home
            return
        
        if user.type == 'patient':
            user = Patient.get_user(login_name)
            
        return redirect('/health_appointment/patient_home/'+str(user.user_id))
