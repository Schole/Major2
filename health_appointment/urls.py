from django.urls import path

from .views import (
    SelectIllnessView,
    ViewAvailableAppointment,
    ConfirmAppointment,
    CreateAppointment,
)


urlpatterns = [
    path('', SelectIllnessView.as_view(), name='home'),
    path('select/', SelectIllnessView.as_view(), name='select_illness'),
    path('availability/', ViewAvailableAppointment.as_view(), name='availability'),
    path('no_availability/', ViewAvailableAppointment.as_view(), name='no_availability'),
    path('confirm_appointment_selection/', ConfirmAppointment.as_view(), name='confirm_appointment_selection'),
    path('create_appointment_success/', CreateAppointment.as_view(), name='create_appointment_success'),
]