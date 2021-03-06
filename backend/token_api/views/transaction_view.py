from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from ..models.token_models.transaction import Transaction
from ..token_services.template_serializer import serialize_general
from ..common.util import *


@csrf_exempt
@require_http_methods(["POST"])
def get_transactions(request):

    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not application_name:
        return JsonResponse({'message': "No application provided"}, status=400)

    return JsonResponse({'message': serialize_general(Transaction.objects.filter(application__application_name=application_name))})