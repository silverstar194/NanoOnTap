from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models.deletion import ProtectedError
from django.core.exceptions import ObjectDoesNotExist


from ..models.token_models.token import Token
from ..token_services.template_serializer import serialize_tokens
from ..token_services.template_deserializer import deserializer_tokens
from ..common.util import *


@csrf_exempt
@require_http_methods(["POST"])
def get_tokens(request):

    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    if not application_name:
        return JsonResponse({'message': "No application provided"})

    return JsonResponse({'message': serialize_tokens(Token.objects.filter(application__application_name=application_name))})


@csrf_exempt
@require_http_methods(["POST"])
def get_token(request):

    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    if not application_name:
        return JsonResponse({'message': "No application provided"})

    try:
        token_name = parse_arg(request, "token_name")
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    if not token_name:
        return JsonResponse({'message': "No token_name provided"})

    try:
        device = Token.objects.get(application__application_name=application_name, token_name=token_name)
    except ObjectDoesNotExist:
        return JsonResponse({'message': serialize_tokens([])})

    return JsonResponse({'message': serialize_tokens([device])})


@csrf_exempt
@require_http_methods(["POST"])
def update_token(request):

    try:
        token = parse_json(request)
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    try:
        deserializer_tokens([token])
    except Exception:
        return JsonResponse({"message": "Invalid token object"})

    return JsonResponse({"message": "Token updated"})


@csrf_exempt
@require_http_methods(["POST"])
def remove_token(request):
    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    if not application_name:
        return JsonResponse({'message': "No application provided"})

    try:
        token_name = parse_arg(request, "token_name")
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    if not token_name:
        return JsonResponse({'message': "No token_name provided"})

    try:
        Token.objects.get(application__application_name=application_name, token_name=token_name).delete()
    except ProtectedError as e:
        return JsonResponse({'message': str(e)}, status=403)

    return JsonResponse({'message': "Token removed"})

