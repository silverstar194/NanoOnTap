from django.views.decorators.csrf import csrf_exempt

from ..models.nano_models.wallet import Wallet
from ..token_services.template_serializer import serialize_wallets
from ..token_services.template_deserializer import deserializer_wallets
from ..common.util import *
from django.views.decorators.http import require_http_methods

from django.db.models.deletion import ProtectedError
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
@require_http_methods(["POST"])
def get_wallets(request):

    application_name = parse_arg(request, "application")

    return JsonResponse({'message': serialize_wallets(Wallet.objects.filter(application__application_name=application_name))})


@csrf_exempt
@require_http_methods(["POST"])
def get_wallet(request):

    application_name = parse_arg(request, "application")
    wallet_name = parse_arg(request, "wallet_name")

    try:
        wallet = Wallet.objects.get(application__application_name=application_name, wallet_name=wallet_name)
    except ObjectDoesNotExist:
        return JsonResponse({'message': serialize_wallets([])})

    return JsonResponse({'message': serialize_wallets([wallet])})


@csrf_exempt
@require_http_methods(["POST"])
def update_wallet(request):

    wallet = parse_json(request)
    deserializer_wallets([wallet])

    return JsonResponse({"message": "Wallet updated"})


@csrf_exempt
@require_http_methods(["POST"])
def remove_wallet(request):
    application_name = parse_arg(request, "application")
    wallet_name = parse_arg(request, "wallet_name")

    try:
        Wallet.objects.get(application__application_name=application_name, wallet_name=wallet_name).delete()
    except ProtectedError as e:
        return JsonResponse({'message': str(e)}, status=403)

    return JsonResponse({'message': "Wallet removed"})

