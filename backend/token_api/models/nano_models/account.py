from django.db import models

from .wallet import Wallet

from ..token_models.account_policy import AccountPolicy

from ..token_models.application import Application

from rest_framework import serializers


class AccountManager(models.Manager):
    def get_by_natural_key(self, account_id):
        return self.get(account_id=account_id)


class Account(models.Model):
    account_id = models.CharField(max_length=64)

    wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True)

    address = models.CharField(max_length=65)

    current_balance = models.DecimalField(default=0, decimal_places=16, max_digits=64)

    POW = models.CharField(max_length=16, null=True, default=None)

    application = models.ForeignKey(Application, related_name="account_application", on_delete=models.SET_NULL, null=True)

    account_policies = models.ManyToManyField(AccountPolicy, related_name="account_policies")

    objects = AccountManager()

    class Meta:
        unique_together = [['account_id', 'application',]]

    def natural_key(self):
        return (self.account_id, )

    def __str__(self):
        return "{0} : {1}".format(self.account_id, self.address)

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ('address', 'current_balance', 'POW', )
