import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .token_services.template import export_template, import_template
from .token_services.application import clean_up_failed_template, application_exists

from .token_services.device import get_device
from .token_services.token import get_token
from .token_services.application import get_application

from .token_services.executor import Executor
from .token_services.bootstrap import Bootstrap

import logging
logger = logging.getLogger(__name__)

@csrf_exempt
def import_template_view(request):
    if request.method == 'POST':
        data = request.body.decode()
        json_data = json.loads(data)

        if "application" not in json_data:
            return JsonResponse({'message': "No application provided"})

        application = json_data["application"][0]["fields"]["application_id"]
        result = import_template(data)

        if not result:
            clean_up_failed_template(application)
            return JsonResponse({'message': "Application {0} failed".format(application)})

        bootstrapper = Bootstrap(application)
        bootstrapper.bootstrap_application()

        if application_exists(application):
            return JsonResponse({'message': "Application {0} already exists. Template changes applied.".format(application)})

        return JsonResponse({'message': "Application {0} accepted and created".format(application)}, status=200)

    return JsonResponse({'message': "Post only requests for application creation"}, status=403)


@csrf_exempt
def export_template_view(request):
    if request.method == 'POST':
         data = request.body.decode('utf-8')
         received_json_data = json.loads(data)

         if "application" in received_json_data:
             application = received_json_data["application"]
             return JsonResponse(export_template(application), safe=False)

         return JsonResponse({'message': "No application in request"}, status=403)

    return JsonResponse({'message': "Post only requests"}, status=403)

@csrf_exempt
def attempt_action(request):
    if request.method == 'POST':
         data = request.body.decode('utf-8')
         received_json_data = json.loads(data)

         application_id = received_json_data["application"]
         device_id = received_json_data["device"]
         token_id = received_json_data["token"]

         device = get_device(device_id, application_id)
         token = get_token(token_id, application_id)
         application = get_application(application_id)

         action_set_executor = Executor(device, token, application)
         action_set_executor.run_action_set()

         return JsonResponse({'message': "Action complete"}, status=403)

    return JsonResponse({'message': "Post requests only"}, status=403)

