from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

import logging
from collections.abc import Iterable

from ..token_services.device import get_device
from ..token_services.token import get_token
from ..token_services.application import get_application
from ..token_services.executor import Executor
from ..token_services.template_serializer import serialize_action_set_history
from ..common.util import *

logger = logging.getLogger(__name__)


@csrf_exempt
def ping(request):
    return JsonResponse({"message": "pong"})


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

    if not device:
        return JsonResponse({'message': "Device '{0}' does not exist.".format(device_name)}, status=400)

    token = get_token(token_name, application_name)

    if not token:
        return JsonResponse({'message': "Token '{0}' does not exist.".format(token_name)}, status=400)

    application = get_application(application_name)

    if not token:
        return JsonResponse({'message': "Application '{0}' does not exist.".format(application_name)}, status=400)

    action_set_executor = Executor(device, token, application)

    output = {}
    action_set_history = action_set_executor.run_action_set()

    action_set_history = action_set_history if isinstance(action_set_history, Iterable) else [action_set_history]
    logger.info(action_set_history)

    output['message'] = serialize_action_set_history(action_set_history)

    return JsonResponse(output)
