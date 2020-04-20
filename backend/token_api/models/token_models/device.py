from django.db import models


from .action_set import ActionSet
from .application import Application


class DeviceManager(models.Manager):
    def get_by_natural_key(self, device_name):
        return self.get(device_name=device_name)


class Device(models.Model):
    device_name = models.CharField(max_length=64)

    application = models.ForeignKey(Application, related_name="device_application", on_delete=models.SET_NULL, null=True)

    action_sets = models.ManyToManyField(ActionSet, related_name="device_action_sets")

    objects = DeviceManager()

    class Meta:
        unique_together = [['device_name', 'application']]

    def __str__(self):
        return "{0}".format(self.device_name)

    def natural_key(self):
        return (self.device_name,)