from django.http import JsonResponse

from decimal import *
import json


def convert_raw_to_NANO(raw_amount):
    raw_amount_to_one_nano = 1000000000000000000000000000000
    return (1.0*raw_amount) / raw_amount_to_one_nano


def convert_NANO_to_RAW(NANO_amount):
    raw_amount_to_one_nano = 1000000000000000000000000000000
    return "{:0f}".format(Decimal(Decimal(NANO_amount) * Decimal(raw_amount_to_one_nano)))


def parse_json(request):
    data = request.body.decode()
    json_data = json.loads(data)
    return json_data


def parse_arg(request, arg):
    json_data = parse_json(request)
    if arg not in json_data:
        return JsonResponse({'message': "No {0} provided".format(arg)})
    return json_data[arg]
