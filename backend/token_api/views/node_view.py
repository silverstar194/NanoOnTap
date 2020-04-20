from django.views.decorators.csrf import csrf_exempt

from ..models.nano_models.node import Node
from ..token_services.template_serializer import serialize_nodes
from ..token_services.template_deserializer import deserializer_nodes
from ..common.util import *
from django.views.decorators.http import require_http_methods

from django.db.models.deletion import ProtectedError
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
@require_http_methods(["POST"])
def get_nodes(request):

    application_name = parse_arg(request, "application")

    return JsonResponse({'message': serialize_nodes(Node.objects.filter(application__application_name=application_name))})


@csrf_exempt
@require_http_methods(["POST"])
def get_node(request):

    application_name = parse_arg(request, "application")
    node_name = parse_arg(request, "node_name")

    try:
        node = Node.objects.get(application__application_name=application_name, node_name=node_name)
    except ObjectDoesNotExist:
        return JsonResponse({'message': serialize_nodes([])})

    return JsonResponse({'message': serialize_nodes([node])})


@csrf_exempt
@require_http_methods(["POST"])
def update_node(request):

    account = parse_json(request)
    deserializer_nodes([account])

    return JsonResponse({"message": "Node updated"})


@csrf_exempt
@require_http_methods(["POST"])
def remove_node(request):
    application_name = parse_arg(request, "application")
    node_name = parse_arg(request, "node_name")

    try:
        Node.objects.get(application__application_name=application_name, node_name=node_name).delete()
    except ProtectedError as e:
        return JsonResponse({'message': str(e)}, status=403)

    return JsonResponse({'message': "Node removed"})

