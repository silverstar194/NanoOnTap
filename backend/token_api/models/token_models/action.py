from django.db import models

from ..nano_models.account import Account

from .application import Application


class ActionPolicyManager(models.Manager):
    def get_by_natural_key(self, action_name):
        return self.get(action_name=action_name)


class Action(models.Model):

    action_name = models.CharField(max_length=64)

    from_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="from_account")

    to_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="to_account")

    amount = models.IntegerField(default=0)  # Measured in RAW

    application = models.ForeignKey(Application, related_name="action_application", on_delete=models.PROTECT)

    objects = ActionPolicyManager()

    priority = models.IntegerField()

    class Meta:
        unique_together = [['action_name', 'application']]
        ordering = ['priority']

    def natural_key(self):
        return (self.action_name, )

    def __str__(self):
        return "{0}: {1} NANO from {2} to {3}".format(self.action_name, self.amount, self.from_account.address,
                                                               self.to_account.address)
