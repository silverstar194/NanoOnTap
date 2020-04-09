from django.db import models

from .account import Account

from ..token_models.application import Application


class Transaction(models.Model):
    origin = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='origin')

    destination = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='destination')

    timestamp = models.BigIntegerField(null=True, default=None)

    amount = models.DecimalField(default=0, decimal_places=0, max_digits=38)  # Measured in RAW

    transaction_hash_sending = models.CharField(max_length=64)

    transaction_hash_receiving = models.CharField(max_length=64)

    application = models.ForeignKey(Application, related_name="transaction_application", on_delete=models.PROTECT)

    def __str__(self):
        return u'Amount: %s\nOrigin: %s\nDestination: %s\nOrigin Hash: %s\nDestination Hash: %s' % (self.amount, self.origin.address, self.destination.address, self.transaction_hash_sending, self.transaction_hash_receiving)
