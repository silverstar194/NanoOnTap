from django.db import models

from .application import Application


class AccountPolicyManager(models.Manager):
    def get_by_natural_key(self, policy_name):
        return self.get(policy_name=policy_name)


class AccountPolicy(models.Model):

    policy_name = models.CharField(max_length=64)

    application = models.ForeignKey(Application, related_name="account_policy_application", on_delete=models.PROTECT)

    send_action_limit = models.IntegerField(default=-1)

    receive_action_limit = models.IntegerField(default=-1)

    send_amount_limit = models.IntegerField(default=-1)

    receive_amount_limit = models.IntegerField(default=-1)

    objects = AccountPolicyManager()

    class Meta:
        unique_together = [['policy_name', 'application']]

    """
    Custom logic around when an account can be used
    """
    def allow_account_usage(self):
        return True

    def __str__(self):
        return "Policy: "+str(self.policy_name)

    def natural_key(self):
        return (self.policy_name, )
