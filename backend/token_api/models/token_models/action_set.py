from django.db import models

from .application import Application

from .action import Action

class ActionSetPolicyManager(models.Manager):
    def get_by_natural_key(self, action_set_name):
        return self.get(action_set_name=action_set_name)


class ActionSet(models.Model):

    action_set_name = models.CharField(max_length=64)

    priority = models.IntegerField()

    application = models.ForeignKey(Application, related_name="action_set_application", on_delete=models.PROTECT)

    actions = models.ForeignKey(Action, related_name="actions", on_delete=models.PROTECT)

    objects = ActionSetPolicyManager()

    class Meta:
        unique_together = [['action_set_name', 'application']]
        ordering = ['priority']

    def natural_key(self):
        return (self.action_set_name, )

    def __str__(self):
        return "Action Set {0} Priority {1}".format(self.action_set_name, self.priority)
