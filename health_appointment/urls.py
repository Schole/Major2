from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import (
    HomeView,
    PatientHomeView,
    SelectIllnessView,
    CheckAvailableAppointmentView,
    CreateAppointmentView,
    CancelAppointmentView,
)


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('patient_home/', PatientHomeView.as_view(), name='patient_home'),
    path('patient_home/<uuid:user_id>/', PatientHomeView.as_view(), name='patient_home'),
    path('select/', SelectIllnessView.as_view(), name='select_illness'),
    path('create_appointment/', CheckAvailableAppointmentView.as_view(), name='create_appointment'),
    path('cancel_appointment/', CancelAppointmentView.as_view(), name='cancel_appointment'),
    path('no_availability/', CheckAvailableAppointmentView.as_view(), name='no_availability'),
    path('create_appointment_success/', CreateAppointmentView.as_view(), name='create_appointment_success'),
]