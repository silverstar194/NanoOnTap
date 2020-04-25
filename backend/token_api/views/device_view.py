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

    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    if not application_name:
        return JsonResponse({'message': "No application provided"})

    return JsonResponse({'message': serialize_devices(Device.objects.filter(application__application_name=application_name))})


@csrf_exempt
@require_http_methods(["POST"])
def get_device(request):

    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    if not application_name:
        return JsonResponse({'message': "No application provided"})

    try:
        device_name = parse_arg(request, "device_name")
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    if not device_name:
        return JsonResponse({'message': "No device_name provided"})

    try:
        device = Device.objects.get(application__application_name=application_name, device_name=device_name)
    except ObjectDoesNotExist:
        return JsonResponse({'message': serialize_devices([])})

    return JsonResponse({'message': serialize_devices([device])})


@csrf_exempt
@require_http_methods(["POST"])
def update_device(request):

    try:
        device = parse_json(request)
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    try:
        deserializer_devices([device])
    except Exception:
        return JsonResponse({"message": "Invalid device object"})

    return JsonResponse({"message": "Device updated"})


@csrf_exempt
@require_http_methods(["POST"])
def remove_device(request):
    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    if not application_name:
        return JsonResponse({'message': "No application provided"})

    try:
        device_name = parse_arg(request, "device_name")
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    if not device_name:
        return JsonResponse({'message': "No device_name provided"})

    try:
        Device.objects.get(application__application_name=application_name, device_name=device_name).delete()
    except ProtectedError as e:
        return JsonResponse({'message': str(e)}, status=403)

    return JsonResponse({'message': "Device removed"})

