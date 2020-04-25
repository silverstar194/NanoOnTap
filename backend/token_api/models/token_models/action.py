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

    amount = models.DecimalField(default=0, decimal_places=16, max_digits=64)

    application = models.ForeignKey(Application, related_name="action_application", on_delete=models.SET_NULL, null=True)

    objects = ActionPolicyManager()

    priority = models.IntegerField()

    class Meta:
        unique_together = [['action_name', 'application']]
        ordering = ['priority']

    def __str__(self):
        return "{0}: {1} NANO from {2} to {3}".format(self.action_name, self.amount, self.from_account.account_name,
                                                               self.to_account.account_name)

    def natural_key(self):
        return (self.action_name,)
