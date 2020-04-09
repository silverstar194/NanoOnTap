from django.db import models

class AccountPolicy(models.Model):

    policy_name = models.CharField(max_length=64)

    application = models.CharField(max_length=64)

    class Meta:
        unique_together = ('policy_name', 'application',)

    def allow_account_usage(self):
        return True

    def __str__(self):
        return str(self.allow_account_usage())

    def natural_key(self):
        return self.policy_name