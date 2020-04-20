from django.views.decorators.csrf import csrf_exempt

from ..models.token_models.action_policy import ActionPolicy
from ..token_services.template_serializer import serialize_action_policies
from ..token_services.template_deserializer import deserializer_action_polices
from ..common.util import *
from django.views.decorators.http import require_http_methods

from django.db.models.deletion import ProtectedError
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
@require_http_methods(["POST"])
def get_action_policies(request):

    application_name = parse_arg(request, "application")

    return JsonResponse({'message': serialize_action_policies(ActionPolicy.objects.filter(application__application_name=application_name))})


@csrf_exempt
@require_http_methods(["POST"])
def get_action_policy(request):

    application_name = parse_arg(request, "application")
    policy_name = parse_arg(request, "policy_name")

    try:
        account_policy = ActionPolicy.objects.get(application__application_name=application_name, policy_name=policy_name)
    except ObjectDoesNotExist:
        return JsonResponse({'message': serialize_action_policies([])})

    return JsonResponse({'message': serialize_action_policies([account_policy])})


@csrf_exempt
@require_http_methods(["POST"])
def update_action_policy(request):

    action_policy = parse_json(request)
    deserializer_action_polices([action_policy])

    return JsonResponse({"message": "Action Policy updated"})


@csrf_exempt
@require_http_methods(["POST"])
def remove_action_policy(request):
    application_name = parse_arg(request, "application")
    policy_name = parse_arg(request, "policy_name")

    try:
        ActionPolicy.objects.get(application__application_name=application_name, policy_name=policy_name).delete()
    except ProtectedError as e:
        return JsonResponse({'message': str(e)}, status=403)

    return JsonResponse({'message': "Action Policy removed"})

