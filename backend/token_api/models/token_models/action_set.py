from django.db import models

from .application import Application

from .action import Action


class ActionSetManager(models.Manager):
    def get_by_natural_key(self, action_set_name):
        return self.get(action_set_name=action_set_name)


class ActionSet(models.Model):
    action_set_name = models.CharField(max_length=64)

    priority = models.IntegerField()

    application = models.ForeignKey(Application, related_name="action_set_application", on_delete=models.SET_NULL, null=True)

    actions = models.ManyToManyField(Action, related_name="actions")

    objects = ActionSetManager()

    class Meta:
        unique_together = [['action_set_name', 'application']]
        ordering = ['priority']

    def __str__(self):
        return "{0}: Priority {1}".format(self.action_set_name, self.priority)

    def natural_key(self):
        return (self.action_set_name,)
