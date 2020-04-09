from django.db import models

from .account import Account


class ActionPolicyManager(models.Manager):
    def get_by_natural_key(self, policy_name):
        return self.get(policy_name=policy_name)

class ActionPolicy(models.Model):

    policy_name = models.CharField(max_length=64)

    allowed_from_accounts = models.ManyToManyField(Account, related_name="allowed_from_accounts")
    allowed_to_accounts = models.ManyToManyField(Account, related_name="allowed_to_accounts")

    denied_from_accounts = models.ManyToManyField(Account, related_name="denied_from_accounts")
    denied_to_accounts = models.ManyToManyField(Account, related_name="denied_to_accounts")

    allowed_devices = models.ManyToManyField(Account, related_name="allowed_devices")
    denied_devices = models.ManyToManyField(Account, related_name="denied_devices")

    priority = models.IntegerField()

    application = models.CharField(max_length=64)

    objects = ActionPolicyManager()

    class Meta:
        unique_together = [['policy_name', 'application']]

    def device_allowed(self, device):
        return not self.allowed_devices or (device in self.allowed_devices.all() and device not in self.denied_devices)

    def from_account_allowed(self, account):
        return not self.allowed_from_accounts or (account in self.allowed_from_accounts.all() and account not in self.denied_from_accounts)

    def to_account_allowed(self, account):
        return not self.allowed_to_accounts or (account in self.allowed_to_accounts.all() and account not in self.denied_to_accounts)

    def __str__(self):
        return "Allowed from accounts {0} \n Denied from account {1} \n Allowed to accounts {2} \n Denied to accounts {3} \n Allowed devices {4} \n Denied devices {5} \n Priority {7}"\
            .format(self.allowed_from_accounts.count() if self.allowed_from_accounts else 0,
                    self.denied_from_accounts.count() if self.denied_from_accounts else 0,
                    self.allowed_to_accounts.count() if self.allowed_to_accounts else 0,
                    self.denied_to_accounts.count() if self.denied_to_accounts else 0,
                    self.allowed_devices.count() if self.allowed_devices else 0,
                    self.denied_devices.count() if self.denied_devices else 0,
                    self.priority)

    def natural_key(self):
        return (self.policy_name,)
