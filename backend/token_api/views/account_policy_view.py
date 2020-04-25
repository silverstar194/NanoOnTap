from django.views.decorators.csrf import csrf_exempt
from django.db.models.deletion import ProtectedError
from django.core.exceptions import ObjectDoesNotExist


from ..models.token_models.account_policy import AccountPolicy
from ..token_services.template_serializer import serialize_account_policies
from ..token_services.template_deserializer import deserializer_account_policies
from ..common.util import *
from django.views.decorators.http import require_http_methods


@csrf_exempt
@require_http_methods(["POST"])
def get_account_policies(request):

    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    if not application_name:
        return JsonResponse({'message': "No application provided"})

    return JsonResponse({'message': serialize_account_policies(AccountPolicy.objects.filter(application__application_name=application_name))})


@csrf_exempt
@require_http_methods(["POST"])
def get_account_policy(request):

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
        account_policy = AccountPolicy.objects.get(application__application_name=application_name, policy_name=policy_name)
    except ObjectDoesNotExist:
        return JsonResponse({'message': serialize_account_policies([])})

    return JsonResponse({'message': serialize_account_policies([account_policy])})


@csrf_exempt
@require_http_methods(["POST"])
def update_account_policy(request):
    try:
        account_policy = parse_json(request)
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    try:
        deserializer_account_policies([account_policy])
    except Exception:
        return JsonResponse({"message": "Invalid account policy object"})

    return JsonResponse({"message": "Account Policy updated"})


@csrf_exempt
@require_http_methods(["POST"])
def remove_account_policy(request):
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
        AccountPolicy.objects.get(application__application_name=application_name, policy_name=policy_name).delete()
    except ProtectedError as e:
        return JsonResponse({'message': str(e)}, status=403)

    return JsonResponse({'message': "Account Policy removed"})

