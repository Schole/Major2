from typing import Dict
from django.http import HttpResponse
from django.template import loader
from django.db.models.query import QuerySet


def send_http_request(request, context: Dict[str,any], template: str) -> HttpResponse:

    template = loader.get_template(template)

    return HttpResponse(
        template.render(
            context,
            request
        )
    )