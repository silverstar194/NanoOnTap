from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

import logging

from ..nano_services.balance_accounts_service import BalanceAccount
from ..nano_services.account_service import AccountService

from ..common.util import *

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def sync(request):
    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not application_name:
        return JsonResponse({'message': "No application provided"}, status=400)

    BalanceAccount().sync_accounts()
    AccountService.clear_receive_accounts()

    return JsonResponse({'message': "Sync complete"})
