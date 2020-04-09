from django.db import models

from .action import Action


class Device(models.Model):
    device_id = models.CharField(max_length=64)

    application = models.CharField(max_length=64)

    actions = models.ManyToManyField(Action, related_name="action")

    class Meta:
        unique_together = ('device_id', 'application')

    def __str__(self):
        return "Device {0}".format(self.device_id)

    def natural_key(self):
        self.device_id