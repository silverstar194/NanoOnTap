from django.db import models

from .node import Node

from .application import Application

class WalletManager(models.Manager):
    def get_by_natural_key(self, wallet_id):
        return self.get(wallet_id=wallet_id)


class Wallet(models.Model):
    node = models.ForeignKey(Node, on_delete=models.PROTECT)

    wallet_id = models.CharField(max_length=64)

    application = models.ForeignKey(Application, related_name="wallet_application", on_delete=models.PROTECT)

    objects = WalletManager()

    def __str__(self):
        return u'%s' % (self.wallet_id)

    def natural_key(self):
        return (self.wallet_id,)