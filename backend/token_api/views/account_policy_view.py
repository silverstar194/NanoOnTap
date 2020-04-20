from django.views.decorators.csrf import csrf_exempt

from ..models.token_models.account_policy import AccountPolicy
from ..token_services.template_serializer import serialize_account_policies
from ..token_services.template_deserializer import deserializer_account_policies
from ..common.util import *
from django.views.decorators.http import require_http_methods

from django.db.models.deletion import ProtectedError
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
@require_http_methods(["POST"])
def get_account_policies(request):

    application_name = parse_arg(request, "application")

    return JsonResponse({'message': serialize_account_policies(AccountPolicy.objects.filter(application__application_name=application_name))})


@csrf_exempt
@require_http_methods(["POST"])
def get_account_policy(request):

    application_name = parse_arg(request, "application")
    policy_name = parse_arg(request, "policy_name")

    try:
        account_policy = AccountPolicy.objects.get(application__application_name=application_name, policy_name=policy_name)
    except ObjectDoesNotExist:
        return JsonResponse({'message': serialize_account_policies([])})

    return JsonResponse({'message': serialize_account_policies([account_policy])})


@csrf_exempt
@require_http_methods(["POST"])
def update_account_policy(request):

    account_policy = parse_json(request)
    deserializer_account_policies([account_policy])

    return JsonResponse({"message": "Account Policy updated"})


@csrf_exempt
@require_http_methods(["POST"])
def remove_account_policy(request):
    application_name = parse_arg(request, "application")
    policy_name = parse_arg(request, "policy_name")

    try:
        AccountPolicy.objects.get(application__application_name=application_name, policy_name=policy_name).delete()
    except ProtectedError as e:
        return JsonResponse({'message': str(e)}, status=403)

    return JsonResponse({'message': "Account Policy removed"})

