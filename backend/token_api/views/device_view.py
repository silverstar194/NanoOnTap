from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models.deletion import ProtectedError
from django.core.exceptions import ObjectDoesNotExist


from ..models.token_models.device import Device
from ..token_services.template_serializer import serialize_devices
from ..token_services.template_deserializer import deserializer_devices
from ..common.util import *


@csrf_exempt
@require_http_methods(["POST"])
def get_devices(request):

    application_name = parse_arg(request, "application")

    return JsonResponse({'message': serialize_devices(Device.objects.filter(application__application_name=application_name))})


@csrf_exempt
@require_http_methods(["POST"])
def get_device(request):

    application_name = parse_arg(request, "application")
    device_name = parse_arg(request, "device_name")

    try:
        device = Device.objects.get(application__application_name=application_name, device_name=device_name)
    except ObjectDoesNotExist:
        return JsonResponse({'message': serialize_devices([])})

    return JsonResponse({'message': serialize_devices([device])})


@csrf_exempt
@require_http_methods(["POST"])
def update_device(request):

    device = parse_json(request)
    deserializer_devices([device])

    return JsonResponse({"message": "Device updated"})


@csrf_exempt
@require_http_methods(["POST"])
def remove_device(request):
    application_name = parse_arg(request, "application")
    device_name = parse_arg(request, "device_name")

    try:
        Device.objects.get(application__application_name=application_name, device_name=device_name).delete()
    except ProtectedError as e:
        return JsonResponse({'message': str(e)}, status=403)

    return JsonResponse({'message': "Device removed"})

