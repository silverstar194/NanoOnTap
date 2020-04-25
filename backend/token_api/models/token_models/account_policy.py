from django.db import models


from .application import Application


class AccountPolicyManager(models.Manager):
    def get_by_natural_key(self, policy_name):
        return self.get(policy_name=policy_name)


class AccountPolicy(models.Model):

    policy_name = models.CharField(max_length=64)

    application = models.ForeignKey(Application, related_name="account_policy_application", on_delete=models.SET_NULL, null=True)

    send_action_limit = models.IntegerField(default=-1)

    receive_action_limit = models.IntegerField(default=-1)

    send_amount_limit = models.DecimalField(default=-1, decimal_places=16, max_digits=64)

    receive_amount_limit = models.DecimalField(default=-1, decimal_places=16, max_digits=64)

    objects = AccountPolicyManager()

    class Meta:
        unique_together = [['policy_name', 'application']]

    """
    Custom logic around when an account can be used
    """
    def allow_account_usage(self):
        return True

    def __str__(self):
        return "{0}: Send Action Limit {1} Receive Action Limit {1} Send Amount Limit {3} Receive Amount Limit {4}".format(self.policy_name, self.send_action_limit, self.receive_action_limit, self.send_amount_limit, self.receive_amount_limit)

    def natural_key(self):
        return (self.policy_name, )
