from django.db import models

from .wallet import Wallet

from ..token_models.account_policy import AccountPolicy

from ..token_models.application import Application


class AccountManager(models.Manager):
    def get_by_natural_key(self, address):
        return self.get(address=address)


class Account(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)

    address = models.CharField(max_length=64)

    current_balance = models.IntegerField(default=0)  # Measured in RAW

    POW = models.CharField(max_length=16, null=True, default=None)
    in_use = models.BooleanField(default=False)

    application = models.ForeignKey(Application, related_name="account_application", on_delete=models.PROTECT)

    account_policies = models.ManyToManyField(AccountPolicy, related_name="account_policies")

    objects = AccountManager()

    class Meta:
        unique_together = [['address', 'application']]

    def natural_key(self):
           return (self.address,)

    def __str__(self):
        return u'%s' % (self.address)

    def lock(self):
        self.in_use = True
        self.save()

    def unlock(self):
        self.in_use = False
        self.save()
