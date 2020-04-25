from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from ..nano_services.transaction_service import InsufficientNanoException
from ..nano_services.transaction_service import NegativeNanoException
from ..nano_services.transaction_service import RCPException
from ..nano_services.transaction_service import InvalidPOWException

import logging


from ..token_services.template_serializer import export_template
from ..token_services.template_deserializer import import_template
from ..token_services.application import clean_up_failed_template, application_exists
from ..token_services.device import get_device
from ..token_services.token import get_token
from ..token_services.application import get_application
from ..token_services.executor import Executor
from ..token_services.bootstrap import Bootstrap
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

    bootstrapper = Bootstrap(application_name)
    bootstrapper.bootstrap_application()

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


@csrf_exempt
@require_http_methods(["POST"])
def attempt_action(request):
    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not application_name:
        return JsonResponse({'message': "No application provided"}, status=400)

    try:
        device_name = parse_arg(request, "device_name")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not application_name:
        return JsonResponse({'message': "No device_name provided"}, status=400)

    try:
        token_name = parse_arg(request, "token_name")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not application_name:
        return JsonResponse({'message': "No token_name provided"}, status=400)

    device = get_device(device_name, application_name)
    token = get_token(token_name, application_name)
    application = get_application(application_name)

    action_set_executor = Executor(device, token, application)

    try:
        action_set_executor.run_action_set()
    except InsufficientNanoException:
        return JsonResponse({'message': "Action failed. Insufficient Nano."}, status=400)
    except NegativeNanoException:
        return JsonResponse({'message': "Action failed. Nano send amount must be positive."}, status=400)
    except InvalidPOWException:
        return JsonResponse({'message': "Action failed. Total PoW failure."}, status=400)
    except RCPException:
        return JsonResponse({'message': "Action failed. Cannot connect to node."}, status=400)
    except Exception:
        return JsonResponse({'message': "Action failed. Unknown error."}, status=400)

    return JsonResponse({'message': "Action complete"})


