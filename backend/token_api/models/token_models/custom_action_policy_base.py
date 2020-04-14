from django.db import models

from .application import Application


class CustomActionPolicyBaseManager(models.Manager):
    def get_by_natural_key(self, custom_policy_name):
        return self.get(custom_policy_name=custom_policy_name)


class CustomActionPolicyBase(models.Model):
    custom_policy_name = models.CharField(max_length=64)

    priority = models.IntegerField()

    application = models.ForeignKey(Application, related_name="custom_action_policy_application", on_delete=models.PROTECT)

    objects = CustomActionPolicyBaseManager()

    class Meta:
        unique_together = [['custom_policy_name', 'application']]
        ordering = ['priority']

    def __str__(self):
        return self.custom_policy_name
        return "{0} Priority: {6}".format(custom_policy_name, str(self.priority))

    def policy_passed(self, device):
       raise NotImplemented("Implement your custom action policy")

    def natural_key(self):
        return (self.custom_policy_name,)
