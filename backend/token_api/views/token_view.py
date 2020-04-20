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

    application_name = parse_arg(request, "application")

    return JsonResponse({'message': serialize_tokens(Token.objects.filter(application__application_name=application_name))})


@csrf_exempt
@require_http_methods(["POST"])
def get_token(request):

    application_name = parse_arg(request, "application")
    token_name = parse_arg(request, "token_name")

    try:
        device = Token.objects.get(application__application_name=application_name, token_name=token_name)
    except ObjectDoesNotExist:
        return JsonResponse({'message': serialize_tokens([])})

    return JsonResponse({'message': serialize_tokens([device])})


@csrf_exempt
@require_http_methods(["POST"])
def update_token(request):

    device = parse_json(request)
    deserializer_tokens([device])

    return JsonResponse({"message": "Token updated"})


@csrf_exempt
@require_http_methods(["POST"])
def remove_token(request):
    application_name = parse_arg(request, "application")
    token_name = parse_arg(request, "token_name")

    try:
        Token.objects.get(application__application_name=application_name, token_name=token_name).delete()
    except ProtectedError as e:
        return JsonResponse({'message': str(e)}, status=403)

    return JsonResponse({'message': "Token removed"})

