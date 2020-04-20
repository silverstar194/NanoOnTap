from django.views.decorators.csrf import csrf_exempt

from ..models.nano_models.transaction import Transaction
from ..token_services.template_serializer import serialize_general
from ..common.util import *
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["POST"])
def get_transactions(request):

    application_name = parse_arg(request, "application")

    return JsonResponse({'message': serialize_general(Transaction.objects.filter(application__application_name=application_name))})