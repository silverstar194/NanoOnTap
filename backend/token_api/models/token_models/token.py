from django.db import models

from .action_policy import ActionPolicy

from ..custom_action_policies.example_custom_action_policy import CustomActionPolicy

from .application import Application


class TokenManager(models.Manager):
    def get_by_natural_key(self, token_name):
        return self.get(token_name=token_name)


class Token(models.Model):
    token_name = models.CharField(max_length=64)

    application = models.ForeignKey(Application, related_name="token_application", on_delete=models.SET_NULL, null=True)

    action_polices = models.ManyToManyField(ActionPolicy, related_name="action_polices")

    custom_action_polices = models.ManyToManyField(CustomActionPolicy, related_name="custom_action_polices", blank=True)

    objects = TokenManager()

    class Meta:
        unique_together = [['token_name', 'application']]

    def __str__(self):
        return self.token_name

    def natural_key(self):
        return (self.token_name,)