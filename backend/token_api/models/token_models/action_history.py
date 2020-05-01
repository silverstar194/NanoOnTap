from django.db import models


from .action_set import ActionSet
from .action_policy import ActionPolicy
from .application import Application
from .device import Device
from .token import Token
from .transaction import Transaction


class ActionHistory(models.Model):
    action_set = models.ForeignKey(ActionSet, related_name="action_history_action_set", on_delete=models.SET_NULL, null=True)

    policy = models.ForeignKey(ActionPolicy, related_name="action_history_policy", on_delete=models.SET_NULL, null=True)

    executed = models.NullBooleanField(default=False, null=True)

    executed_time = models.DateTimeField(default=None, null=True)

    application = models.ForeignKey(Application, related_name="action_history_application", on_delete=models.SET_NULL, null=True)

    device = models.ForeignKey(Device, related_name="action_history_device", on_delete=models.SET_NULL, null=True)

    token = models.ForeignKey(Token, related_name="action_history_token", on_delete=models.SET_NULL, null=True)

    transactions = models.ManyToManyField(Transaction, related_name="transactions")

    class Meta:
        ordering = ['-executed_time']
