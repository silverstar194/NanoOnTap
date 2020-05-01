from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

import logging


from ..token_services.template_serializer import export_template
from ..token_services.template_deserializer import import_template
from ..token_services.application import clean_up_failed_template, application_exists
from ..common.util import *

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST"])
def import_template_view(request):
    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not application_name:
        return JsonResponse({'message': "No application provided"}, status=400)

    data = request.body.decode()
    result = import_template(data)

    if not result:
        clean_up_failed_template(application_name)
        return JsonResponse({'message': "Application {0} failed".format(application_name)}, status=400)

    if application_exists(application_name):
        return JsonResponse({'message': "Application {0} already exists. Template changes applied.".format(application_name)})

    return JsonResponse({'message': "Application {0} accepted and created".format(application_name)})


@csrf_exempt
@require_http_methods(["POST"])
def export_template_view(request):
     try:
         application_name = parse_arg(request, "application")
     except Exception:
         return JsonResponse({"message": "Invalid json"}, status=400)

     if not application_name:
         return JsonResponse({'message': "No application provided"}, status=400)

     return JsonResponse(export_template(application_name), safe=False)

