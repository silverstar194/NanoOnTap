from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from ..common.util import *
from ..token_services.bootstrap import Bootstrap


@csrf_exempt
@require_http_methods(["POST"])
def bootstrap_all(request):

    try:
        application_name = parse_arg(request, "application")
    except Exception:
        return JsonResponse({"message": "Invalid json"}, status=400)

    if not application_name:
        return JsonResponse({'message': "No application provided"}, status=400)

    try:
        bootstrap = Bootstrap(application_name)
        bootstrap.bootstrap_application()
    except Exception:
        return JsonResponse({"message", "Bootstrap failed"}, status=400)

    return JsonResponse({'message': "Bootstrap complete"})
