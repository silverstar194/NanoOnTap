from django.db import models

from .wallet import Wallet

from .account_policy import AccountPolicy


class Account(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, null=True)

    address = models.CharField(max_length=64)

    current_balance = models.IntegerField(default=0)  # Measured in RAW

    POW = models.CharField(max_length=16, null=True)
    in_use = models.BooleanField(default=False)

    application = models.CharField(max_length=64)

    account_policies = models.ManyToManyField(AccountPolicy, related_name="account_policies")

    class Meta:
        unique_together = ('address', 'application')

    def natural_key(self):
           return self.address

    def __str__(self):
        return u'%s' % (self.address)

    def lock(self):
        self.in_use = True
        self.save()

    def unlock(self):
        self.in_use = False
        self.save()
