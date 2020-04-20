from django.views.decorators.csrf import csrf_exempt

from ..models.token_models.application import Application
from ..token_services.template_serializer import serialize_applications
from ..token_services.template_deserializer import deserializer_applications
from ..common.util import *
from django.views.decorators.http import require_http_methods

from django.db.models.deletion import ProtectedError
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
@require_http_methods(["POST"])
def get_applications(request):

    application_name = parse_arg(request, "application_name")

    return JsonResponse({'message': serialize_applications(Application.objects.filter(application_name=application_name))})


@csrf_exempt
@require_http_methods(["POST"])
def get_application(request):

    application_name = parse_arg(request, "application_name")

    try:
        application = Application.objects.get(application_name=application_name)
    except ObjectDoesNotExist:
        return JsonResponse({'message': serialize_applications([])})

    return JsonResponse({'message': serialize_applications([application])})


@csrf_exempt
@require_http_methods(["POST"])
def update_application(request):

    application = parse_json(request)
    deserializer_applications([application])

    return JsonResponse({"message": "Application updated"})


@csrf_exempt
@require_http_methods(["POST"])
def remove_application(request):
    application_name = parse_arg(request, "application_name")

    try:
        Application.objects.get(application_name=application_name).delete()
    except ProtectedError as e:
        return JsonResponse({'message': str(e)}, status=403)

    return JsonResponse({'message': "Application removed"})

