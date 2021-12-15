from typing import List

from django.http import HttpResponse
from django.views.generic import DetailView
from django.contrib.auth.views import LoginView

from ..models.illness_model import (
    Illness,
    IllnessCategory,
)
from health_appointment.views.util import send_http_request


class SelectIllnessView(LoginView):
    DEFAULT_TEMPLATE = 'health_appointment/select_illness.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        illness_category = IllnessCategory.objects.all()
        illness = Illness.objects.all()

        context = {
            'user_id': request.GET.get('user_id'),
            'illness_categories': illness_category,
            'illnesses': illness
        }
        
        return send_http_request(
            request,
            context,
            self.DEFAULT_TEMPLATE,
        )