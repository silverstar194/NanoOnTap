from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


from ..models.token_models.action_history import ActionHistory
from ..token_services.template_serializer import serialize_general
from ..common.util import *


@csrf_exempt
@require_http_methods(["POST"])
def get_action_history(request):

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

    return JsonResponse({'message': serialize_general(ActionHistory.objects.filter(application__application_name=application_name, action__action_name=action_name))})
