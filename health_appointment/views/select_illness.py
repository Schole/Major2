from typing import List

from django.http import HttpResponse
from django.views.generic import DetailView
from django.template import loader

from ..models.model_illness import (
    Illness,
    IllnessCategory,
    create_illnesses,
    create_illness_category,
)
from ..models.model_user import (
    Doctor,
    Patient,
    create_doctor,
    create_patient
)
from ..models.model_specialty import (
    Specialty,
    SpecialtyCategory,
    create_specialty_category,
    create_specialty,
)


class SelectIllnessView(DetailView):
    DEFAULT_TEMPLATE = 'health_appointment/select_illness.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        # create_illnesses()
        # create_illness_category()
        # create_specialty_category()
        # create_specialty()
        # create_doctor()
        # create_patient()

        template = loader.get_template(self.DEFAULT_TEMPLATE)
        illness_category = IllnessCategory.objects.all()
        illness = Illness.objects.all()

        context = {
            'illness_categories': illness_category,
            'illnesses':illness
        }
        return HttpResponse(
            template.render(
                context,
                request
            )
        )

    def get_illness_categories(self) -> List[IllnessCategory]:
        pass

    def get_illnesses(self) -> List[Illness]:
        pass
