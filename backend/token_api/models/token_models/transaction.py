from django.db import models


from ..nano_models.account import Account
from .application import Application


class Transaction(models.Model):
    origin = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='origin', null=True)

    destination = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='destination', null=True)

    timestamp = models.BigIntegerField(null=True, default=None)

    amount = models.DecimalField(default=0, decimal_places=0, max_digits=64)

    transaction_hash_sending = models.CharField(max_length=64)

    transaction_hash_receiving = models.CharField(max_length=64)

    application = models.ForeignKey(Application, related_name="transaction_application", on_delete=models.SET_NULL, null=True)

    complete = models.NullBooleanField(default=False, null=True)

    error = models.CharField(max_length=265, default=None, null=True)

    def __str__(self):
        return u'Amount: %s\nOrigin: %s\nDestination: %s\nOrigin Hash: %s\nDestination Hash: %s' % (self.amount, self.origin.address, self.destination.address, self.transaction_hash_sending, self.transaction_hash_receiving)
