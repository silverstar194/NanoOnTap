from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models.deletion import ProtectedError
from django.core.exceptions import ObjectDoesNotExist


from ..models.nano_models.node import Node
from ..token_services.template_serializer import serialize_nodes
from ..token_services.template_deserializer import deserializer_nodes
from ..common.util import *


@csrf_exempt
@require_http_methods(["POST"])
def get_nodes(request):

    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    if not application_name:
        return JsonResponse({'message': "No application provided"})

    return JsonResponse({'message': serialize_nodes(Node.objects.filter(application__application_name=application_name))})


@csrf_exempt
@require_http_methods(["POST"])
def get_node(request):

    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    if not application_name:
        return JsonResponse({'message': "No application provided"})

    try:
        node_name = parse_arg(request, "node_name")
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    if not node_name:
        return JsonResponse({'message': "No node_name provided"})

    try:
        node = Node.objects.get(application__application_name=application_name, node_name=node_name)
    except ObjectDoesNotExist:
        return JsonResponse({'message': serialize_nodes([])})

    return JsonResponse({'message': serialize_nodes([node])})


@csrf_exempt
@require_http_methods(["POST"])
def update_node(request):

    try:
        node = parse_json(request)
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    try:
        deserializer_nodes([node])
    except Exception:
        return JsonResponse({"message": "Invalid node object"})

    return JsonResponse({"message": "Node updated"})


@csrf_exempt
@require_http_methods(["POST"])
def remove_node(request):
    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    if not application_name:
        return JsonResponse({'message': "No application provided"})

    try:
        node_name = parse_arg(request, "node_name")
    except Exception:
        return JsonResponse({"message": "Invalid json"})

    if not node_name:
        return JsonResponse({'message': "No node_name provided"})

    try:
        Node.objects.get(application__application_name=application_name, node_name=node_name).delete()
    except ProtectedError as e:
        return JsonResponse({'message': str(e)}, status=403)

    return JsonResponse({'message': "Node removed"})

