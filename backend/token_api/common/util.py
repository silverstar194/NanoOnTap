import json

def parse_json(request):
    data = request.body.decode()
    json_data = json.loads(data)
    return json_data


def parse_arg(request, arg):
    json_data = parse_json(request)
    if arg not in json_data:
        return None
    return json_data[arg]
