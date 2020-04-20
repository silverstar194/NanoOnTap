from django.views.decorators.csrf import csrf_exempt

from ..models.token_models.action import Action
from ..token_services.template_serializer import serialize_actions
from ..token_services.template_deserializer import deserializer_actions
from ..common.util import *
from django.views.decorators.http import require_http_methods

from django.db.models.deletion import ProtectedError
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
@require_http_methods(["POST"])
def get_actions(request):

    application_name = parse_arg(request, "application")

    return JsonResponse({'message': serialize_actions(Action.objects.filter(application__application_name=application_name))})


@csrf_exempt
@require_http_methods(["POST"])
def get_action(request):

    application_name = parse_arg(request, "application")
    action_name = parse_arg(request, "action_name")

    try:
        account = Action.objects.get(application__application_name=application_name, action_name=action_name)
    except ObjectDoesNotExist:
        return JsonResponse({'message': serialize_actions([])})

    return JsonResponse({'message': serialize_actions([account])})


@csrf_exempt
@require_http_methods(["POST"])
def update_action(request):

    account = parse_json(request)
    deserializer_actions([account])

    return JsonResponse({"message": "Action updated"})


@csrf_exempt
@require_http_methods(["POST"])
def remove_action(request):
    application_name = parse_arg(request, "application")
    action_name = parse_arg(request, "action_name")

    try:
        Action.objects.get(application__application_name=application_name, action_name=action_name).delete()
    except ProtectedError as e:
        return JsonResponse({'message': str(e)}, status=403)

    return JsonResponse({'message': "Action removed"})

