from django.views.decorators.csrf import csrf_exempt
from django.db.models.deletion import ProtectedError
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from ..models.nano_models.account import Account
from ..token_services.template_serializer import serialize_accounts
from ..token_services.template_deserializer import deserializer_accounts
from ..common.util import *


@csrf_exempt
@require_http_methods(["POST"])
def get_accounts(request):

    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not application_name:
        return JsonResponse({'message': "No application provided"}, status=400)

    return JsonResponse({'message': serialize_accounts(Account.objects.filter(application__application_name=application_name))})


@csrf_exempt
@require_http_methods(["POST"])
def get_account(request):

    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not application_name:
        return JsonResponse({'message': "No application provided"}, status=400)

    try:
        account_name = parse_arg(request, "account_name")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not account_name:
        return JsonResponse({'message': "No account_name provided"}, status=400)

    try:
        account = Account.objects.get(application__application_name=application_name, account_name=account_name)
    except ObjectDoesNotExist:
        return JsonResponse({'message': serialize_accounts([])})

    return JsonResponse({'message': serialize_accounts([account])})


@csrf_exempt
@require_http_methods(["POST"])
def get_account_balance(request):

    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not application_name:
        return JsonResponse({'message': "No application provided"}, status=400)

    try:
        account_name = parse_arg(request, "account_name")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not account_name:
        return JsonResponse({'message': "No account_name provided"}, status=400)

    try:
        account = Account.objects.get(application__application_name=application_name, account_name=account_name)
    except ObjectDoesNotExist:
        return JsonResponse({'message': []})

    return JsonResponse({'message': {'current_balance': account.current_balance}})


@csrf_exempt
@require_http_methods(["POST"])
def get_account_address(request):

    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not application_name:
        return JsonResponse({'message': "No application provided"}, status=400)

    try:
        account_name = parse_arg(request, "account_name")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not account_name:
        return JsonResponse({'message': "No account_name provided"}, status=400)

    try:
        account = Account.objects.get(application__application_name=application_name, account_name=account_name)
    except ObjectDoesNotExist:
        return JsonResponse({'message': []})

    return JsonResponse({'message': {'address': account.address}})


@csrf_exempt
@require_http_methods(["POST"])
def update_account(request):

    try:
        account = parse_json(request)
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    try:
        deserializer_accounts([account])
    except Exception:
        return JsonResponse({"message": "Invalid account object"}, status=400)

    return JsonResponse({"message": "Account updated"})


@csrf_exempt
@require_http_methods(["POST"])
def remove_account(request):
    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not application_name:
        return JsonResponse({'message': "No application provided"}, status=400)

    try:
        account_name = parse_arg(request, "account_name")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not account_name:
        return JsonResponse({'message': "No account_name provided"}, status=400)

    try:
        Account.objects.get(application__application_name=application_name, account_name=account_name).delete()
    except ProtectedError as e:
        return JsonResponse({'message': str(e)}, status=403)

    return JsonResponse({'message': "Account removed"})

