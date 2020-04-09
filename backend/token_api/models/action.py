from django.db import models

from .account import Account

class Action(models.Model):

    action_name = models.CharField(max_length=64)

    from_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="from_account")
    to_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="to_account")

    amount = models.DecimalField(default=0, decimal_places=0, max_digits=38)  # Measured in RAW

    priority = models.IntegerField()

    application = models.CharField(max_length=64)

    def natural_key(self):
        return self.action_name

    class Meta:
        unique_together = ('action_name', 'application',)

    def __str__(self):
        return "Action Priority {0}: Sending {1} from {2} to {3}".format(self.priority,
                                                                         self.from_account.address,
                                                                         self.to_account.address,
                                                                         self.amount)
