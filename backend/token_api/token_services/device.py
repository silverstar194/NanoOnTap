from .. import models as models

def get_device(device_name, application_name):
    """
    Get device by id

    """
    return models.Device.objects.get(device_name = device_name, application__application_name=application_name)


def get_device_actions(device):
    return models.Action.objects.filter(device=device)
