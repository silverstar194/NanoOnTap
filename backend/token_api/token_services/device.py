from .. import models as models


def get_device(device_name, application_name):
    try:
        return models.Device.objects.get(device_name = device_name, application__application_name=application_name)
    except models.Device.DoesNotExist:
        return None


def get_device_actions(device):
    return models.Action.objects.filter(device=device)
