from django.views.decorators.csrf import csrf_exempt

from ..models.token_models.action_set import ActionSet
from ..token_services.template_serializer import serialize_action_set
from ..token_services.template_deserializer import deserializer_action_set
from ..common.util import *
from django.views.decorators.http import require_http_methods

from django.db.models.deletion import ProtectedError
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
@require_http_methods(["POST"])
def get_action_sets(request):

    application_name = parse_arg(request, "application")

    return JsonResponse({'message': serialize_action_set(ActionSet.objects.filter(application__application_name=application_name))})


@csrf_exempt
@require_http_methods(["POST"])
def get_action_set(request):

    application_name = parse_arg(request, "application")
    action_set_name = parse_arg(request, "action_set_name")

    try:
        account_policy = ActionSet.objects.get(application__application_name=application_name, action_set_name=action_set_name)
    except ObjectDoesNotExist:
        return JsonResponse({'message': serialize_action_set([])})

    return JsonResponse({'message': serialize_action_set([account_policy])})


@csrf_exempt
@require_http_methods(["POST"])
def update_action_set(request):

    action_policy = parse_json(request)
    deserializer_action_set([action_policy])

    return JsonResponse({"message": "Action Set updated"})


@csrf_exempt
@require_http_methods(["POST"])
def remove_action_set(request):
    application_name = parse_arg(request, "application")
    action_set_name = parse_arg(request, "action_set_name")

    try:
        ActionSet.objects.get(application__application_name=application_name, action_set_name=action_set_name).delete()
    except ProtectedError as e:
        return JsonResponse({'message': str(e)}, status=403)

    return JsonResponse({'message': "Action Set removed"})
