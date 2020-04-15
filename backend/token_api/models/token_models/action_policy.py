from django.db import models

from ..nano_models.account import Account
from .device import Device

from .application import Application


class ActionPolicyManager(models.Manager):
    def get_by_natural_key(self, policy_name):
        return self.get(policy_name=policy_name)


class ActionPolicy(models.Model):

    policy_name = models.CharField(max_length=64)

    allowed_from_accounts = models.ManyToManyField(Account, related_name="allowed_from_accounts", blank=True)
    allowed_to_accounts = models.ManyToManyField(Account, related_name="allowed_to_accounts", blank=True)

    denied_from_accounts = models.ManyToManyField(Account, related_name="denied_from_accounts", blank=True)
    denied_to_accounts = models.ManyToManyField(Account, related_name="denied_to_accounts", blank=True)

    allowed_devices = models.ManyToManyField(Device, related_name="allowed_devices", blank=True)
    denied_devices = models.ManyToManyField(Device, related_name="denied_devices", blank=True)

    application = models.ForeignKey(Application, related_name="action_policy_application", on_delete=models.PROTECT)

    action_limit = models.IntegerField(default=-1)

    send_limit = models.IntegerField(default=-1)

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
        return "\n Allowed from accounts: {0} \n Denied from account: {1} \n Allowed to accounts: {2} \n Denied to accounts: {3} \n Allowed devices: {4} \n Denied devices: {5}"\
            .format(self.allowed_from_accounts.count(),
                    self.denied_from_accounts.count(),
                    self.allowed_to_accounts.count(),
                    self.denied_to_accounts.count(),
                    self.allowed_devices.count(),
                    self.denied_devices.count())

    def natural_key(self):
        return (self.policy_name,)
