import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .token_services.template import export_template, import_template
from .token_services.application import application_exists, clean_up_failed_template


@csrf_exempt
def import_template_view(request):
    if request.method == 'POST':
        data = request.body.decode()
        json_data = json.loads(data)

        if "application" not in json_data:
            return JsonResponse({'message': "No application provided"})

        application = json_data["application"]
        if application_exists(application):
            return JsonResponse({'message': "Application {} already exists".format(application)})

        result = import_template(data)

        if not result:
            clean_up_failed_template(application)
            return JsonResponse({'message': "Application {} failed".format(application)})

        return JsonResponse({'message': "Template accepted and created"}, status=200)

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
