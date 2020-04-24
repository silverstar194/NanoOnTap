from django.db import models


from .action import Action
from .action_policy import ActionPolicy
from .application import Application


class ActionHistory(models.Model):
    action = models.OneToOneField(Action, related_name="audit_action", on_delete=models.SET_NULL, null=True)

    policy = models.OneToOneField(ActionPolicy, related_name="audit_policy", on_delete=models.SET_NULL, null=True)

    executed = models.NullBooleanField(default=False, null=True)

    executed_time = models.DateTimeField(default=None, null=True)

    application = models.ForeignKey(Application, related_name="action_history_application", on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-executed_time']
