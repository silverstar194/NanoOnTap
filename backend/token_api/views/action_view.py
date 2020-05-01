from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models.deletion import ProtectedError
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from ..models.token_models.action import Action
from ..token_services.template_serializer import serialize_actions
from ..token_services.template_deserializer import deserializer_actions
from ..common.util import *


@csrf_exempt
@require_http_methods(["POST"])
def get_actions(request):

    try:
        application_name = parse_arg(request, "c")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not application_name:
        return JsonResponse({'message': "No application provided"}, status=400)

    return JsonResponse({'message': serialize_actions(Action.objects.filter(application__application_name=application_name))})


@csrf_exempt
@require_http_methods(["POST"])
def get_action(request):

    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not application_name:
        return JsonResponse({'message': "No application provided"}, status=400)

    try:
        action_name = parse_arg(request, "action_name")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not action_name:
        return JsonResponse({'message': "No action_name provided"}, status=400)

    try:
        account = Action.objects.get(application__application_name=application_name, action_name=action_name)
    except ObjectDoesNotExist:
        return JsonResponse({'message': serialize_actions([])})

    return JsonResponse({'message': serialize_actions([account])})


@csrf_exempt
@require_http_methods(["POST"])
def update_action(request):

    try:
        action = parse_json(request)
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    try:
        deserializer_actions([action])
    except Exception:
        return JsonResponse({"message": "Invalid action object"}, status=400)

    return JsonResponse({"message": "Action updated"})


@csrf_exempt
@require_http_methods(["POST"])
def remove_action(request):
    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not application_name:
        return JsonResponse({'message': "No application provided"}, status=400)

    try:
        action_name = parse_arg(request, "action_name")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not action_name:
        return JsonResponse({'message': "No action_name provided"}, status=400)

    try:
        Action.objects.get(application__application_name=application_name, action_name=action_name).delete()
    except ProtectedError as e:
        return JsonResponse({'message': str(e)}, status=403)

    return JsonResponse({'message': "Action removed"})

