from .. import models as models

def get_device(device_id):
    """
    Get device by id

    """
    return models.Device.objects.get(device_id = device_id)


def get_device_actions(device):
    return models.Action.objects.filter(device=device).order_by("priority")
