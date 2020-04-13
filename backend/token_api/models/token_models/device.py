from django.db import models

from .action_set import ActionSet

from .application import Application


class DeviceManager(models.Manager):
    def get_by_natural_key(self, device_id):
        return self.get(device_id=device_id)


class Device(models.Model):
    device_id = models.CharField(max_length=64)

    application = models.ForeignKey(Application, related_name="device_application", on_delete=models.PROTECT)

    action_sets = models.ManyToManyField(ActionSet, related_name="action")

    objects = DeviceManager()

    class Meta:
        unique_together = [['device_id', 'application']]

    def __str__(self):
        return "Device {0}".format(self.device_id)

    def natural_key(self):
        return (self.device_id,)