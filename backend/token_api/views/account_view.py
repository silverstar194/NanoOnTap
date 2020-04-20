from django.views.decorators.csrf import csrf_exempt

from ..models.nano_models.account import Account
from ..token_services.template_serializer import serialize_accounts
from ..token_services.template_deserializer import deserializer_accounts
from ..common.util import *
from django.views.decorators.http import require_http_methods

from django.db.models.deletion import ProtectedError
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
@require_http_methods(["POST"])
def get_accounts(request):

    application_name = parse_arg(request, "application")

    return JsonResponse({'message': serialize_accounts(Account.objects.filter(application__application_name=application_name))})


@csrf_exempt
@require_http_methods(["POST"])
def get_account(request):

    application_name = parse_arg(request, "application")
    account_name = parse_arg(request, "account_name")

    try:
        account = Account.objects.get(application__application_name=application_name, account_name=account_name)
    except ObjectDoesNotExist:
        return JsonResponse({'message': serialize_accounts([])})

    return JsonResponse({'message': serialize_accounts([account])})


@csrf_exempt
@require_http_methods(["POST"])
def update_account(request):

    account = parse_json(request)
    deserializer_accounts([account])

    return JsonResponse({"message": "Account updated"})


@csrf_exempt
@require_http_methods(["POST"])
def remove_account(request):
    application_name = parse_arg(request, "application")
    account_name = parse_arg(request, "account_name")

    try:
        Account.objects.get(application__application_name=application_name, account_name=account_name).delete()
    except ProtectedError as e:
        return JsonResponse({'message': str(e)}, status=403)

    return JsonResponse({'message': "Account removed"})

