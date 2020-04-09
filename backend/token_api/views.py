from django.shortcuts import render
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .token_services.template import export_template, import_template


@csrf_exempt
def import_template_view(request):
    if request.method == 'POST':
        data = request.body.decode()
        json_data = json.loads(data)

        application = None
        if "application" in json.loads(json_data):
            application = json_data["application"]
        else:
            return JsonResponse({'message': "No application provided"})

        import_template(data)
        return JsonResponse({'message': "Template accepted"},
                            status=200)
    else:
        return JsonResponse({'message': "Post only requests"},
                            status=403)

@csrf_exempt
def export_template_view(request):
    if request.method == 'POST':
         data = request.body.decode('utf-8')
         received_json_data = json.loads(data)

         if "application" in received_json_data:
             application = received_json_data["application"]
             return JsonResponse(export_template(application), safe=False)

         return JsonResponse({'message': "No application in request"},
                             status=403)

    return JsonResponse({'message': "Post only requests"},
                        status=403)
