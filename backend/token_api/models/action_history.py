from django.db import models

from .action import Action
from .action_policy import ActionPolicy


class ActionHistory(models.Model):
    action = models.OneToOneField(Action, related_name="audit_action")

    policy = models.OneToOneField(ActionPolicy, related_name="audit_policy")

    executed = models.NullBooleanField(default=False, null=True)

    executed_time = models.DateTimeField(default=None, null=True)

    application = models.CharField(max_length=64)
