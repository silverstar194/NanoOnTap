from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models.deletion import ProtectedError
from django.core.exceptions import ObjectDoesNotExist


from ..models.token_models.action_policy import ActionPolicy
from ..token_services.template_serializer import serialize_action_policies
from ..token_services.template_deserializer import deserializer_action_polices
from ..common.util import *


@csrf_exempt
@require_http_methods(["POST"])
def get_action_policies(request):

    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    if not application_name:
        return JsonResponse({'message': "No application provided"})

    return JsonResponse({'message': serialize_action_policies(ActionPolicy.objects.filter(application__application_name=application_name))})


@csrf_exempt
@require_http_methods(["POST"])
def get_action_policy(request):

    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    if not application_name:
        return JsonResponse({'message': "No application provided"})

    try:
        policy_name = parse_arg(request, "policy_name")
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    if not policy_name:
        return JsonResponse({'message': "No policy_name provided"})

    try:
        account_policy = ActionPolicy.objects.get(application__application_name=application_name, policy_name=policy_name)
    except ObjectDoesNotExist:
        return JsonResponse({'message': serialize_action_policies([])})

    return JsonResponse({'message': serialize_action_policies([account_policy])})


@csrf_exempt
@require_http_methods(["POST"])
def update_action_policy(request):

    try:
        action_policy = parse_json(request)
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    try:
        deserializer_action_polices([action_policy])
    except Exception:
        return JsonResponse({"message": "Invalid action policy object"})

    return JsonResponse({"message": "Action Policy updated"})


@csrf_exempt
@require_http_methods(["POST"])
def remove_action_policy(request):
    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    if not application_name:
        return JsonResponse({'message': "No application provided"})

    try:
        policy_name = parse_arg(request, "policy_name")
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    if not policy_name:
        return JsonResponse({'message': "No policy_name provided"})

    try:
        ActionPolicy.objects.get(application__application_name=application_name, policy_name=policy_name).delete()
    except ProtectedError as e:
        return JsonResponse({'message': str(e)}, status=403)

    return JsonResponse({'message': "Action Policy removed"})

