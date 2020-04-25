from django.views.decorators.csrf import csrf_exempt
from django.db.models.deletion import ProtectedError
from django.core.exceptions import ObjectDoesNotExist


from ..models.token_models.action_set import ActionSet
from ..token_services.template_serializer import serialize_action_set
from ..token_services.template_deserializer import deserializer_action_set
from ..common.util import *
from django.views.decorators.http import require_http_methods


@csrf_exempt
@require_http_methods(["POST"])
def get_action_sets(request):

    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not application_name:
        return JsonResponse({'message': "No application provided"}, status=400)

    return JsonResponse({'message': serialize_action_set(ActionSet.objects.filter(application__application_name=application_name))})


@csrf_exempt
@require_http_methods(["POST"])
def get_action_set(request):

    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not application_name:
        return JsonResponse({'message': "No application provided"}, status=400)

    try:
        action_set_name = parse_arg(request, "action_set_name")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not action_set_name:
        return JsonResponse({'message': "No action_set_name provided"}, status=400)

    try:
        account_policy = ActionSet.objects.get(application__application_name=application_name, action_set_name=action_set_name)
    except ObjectDoesNotExist:
        return JsonResponse({'message': serialize_action_set([])})

    return JsonResponse({'message': serialize_action_set([account_policy])})


@csrf_exempt
@require_http_methods(["POST"])
def update_action_set(request):

    try:
        action_set = parse_json(request)
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    try:
        deserializer_action_set([action_set])
    except Exception:
        return JsonResponse({"message": "Invalid action set object"}, status=400)

    return JsonResponse({"message": "Action Set updated"})


@csrf_exempt
@require_http_methods(["POST"])
def remove_action_set(request):
    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not application_name:
        return JsonResponse({'message': "No application provided"}, status=400)

    try:
        action_set_name = parse_arg(request, "action_set_name")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not action_set_name:
        return JsonResponse({'message': "No action_set_name provided"}, status=400)

    try:
        ActionSet.objects.get(application__application_name=application_name, action_set_name=action_set_name).delete()
    except ProtectedError as e:
        return JsonResponse({'message': str(e)}, status=403)

    return JsonResponse({'message': "Action Set removed"})

