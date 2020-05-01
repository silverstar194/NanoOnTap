from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models.deletion import ProtectedError
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from ..models.nano_models.wallet import Wallet
from ..token_services.template_serializer import serialize_wallets
from ..token_services.template_deserializer import deserializer_wallets
from ..common.util import *


@csrf_exempt
@require_http_methods(["POST"])
def get_wallets(request):

    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not application_name:
        return JsonResponse({'message': "No application provided"}, status=400)

    return JsonResponse({'message': serialize_wallets(Wallet.objects.filter(application__application_name=application_name))})


@csrf_exempt
@require_http_methods(["POST"])
def get_wallet(request):

    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not application_name:
        return JsonResponse({'message': "No application provided"}, status=400)

    try:
        wallet_name = parse_arg(request, "wallet_name")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not wallet_name:
        return JsonResponse({'message': "No wallet_name provided"}, status=400)

    try:
        wallet = Wallet.objects.get(application__application_name=application_name, wallet_name=wallet_name)
    except ObjectDoesNotExist:
        return JsonResponse({'message': serialize_wallets([])})

    return JsonResponse({'message': serialize_wallets([wallet])})


@csrf_exempt
@require_http_methods(["POST"])
def update_wallet(request):

    try:
        wallet = parse_json(request)
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    try:
        deserializer_wallets([wallet])
    except Exception:
        return JsonResponse({"message": "Invalid wallet object"}, status=400)

    return JsonResponse({"message": "Wallet updated"})


@csrf_exempt
@require_http_methods(["POST"])
def remove_wallet(request):
    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not application_name:
        return JsonResponse({'message': "No application provided"}, status=400)

    try:
        wallet_name = parse_arg(request, "wallet_name")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not wallet_name:
        return JsonResponse({'message': "No wallet_name provided"}, status=400)

    try:
        Wallet.objects.get(application__application_name=application_name, wallet_name=wallet_name).delete()
    except ProtectedError as e:
        return JsonResponse({'message': str(e)}, status=403)

    return JsonResponse({'message': "Wallet removed"})

