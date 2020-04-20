from django.db import models


from .node import Node
from ..token_models.application import Application


class WalletManager(models.Manager):
    def get_by_natural_key(self, wallet_name):
        return self.get(wallet_name=wallet_name)


class Wallet(models.Model):
    node = models.ForeignKey(Node, on_delete=models.SET_NULL, null=True)

    wallet_name = models.CharField(max_length=64, null=True)

    wallet_id = models.CharField(max_length=256)

    application = models.ForeignKey(Application, related_name="wallet_application", on_delete=models.SET_NULL, null=True)

    objects = WalletManager()

    def __str__(self):
        return u'%s' % (self.wallet_name)

    def natural_key(self):
        return (self.wallet_name,)
