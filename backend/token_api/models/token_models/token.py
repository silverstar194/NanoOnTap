from django.db import models

from .action_policy import ActionPolicy

from ..custom_action_policies.example_custom_action_policy import CustomActionPolicy

from .application import Application


class TokenManager(models.Manager):
    def get_by_natural_key(self, token_id):
        return self.get(token_id=token_id)


class Token(models.Model):
    token_id = models.CharField(max_length=64)

    application = models.ForeignKey(Application, related_name="token_application", on_delete=models.PROTECT)

    action_polices = models.ManyToManyField(ActionPolicy, related_name="action_polices")

    custom_action_polices = models.ManyToManyField(CustomActionPolicy, related_name="custom_action_polices", blank=True)

    objects = TokenManager()

    class Meta:
        unique_together = [['token_id', 'application']]

    def __str__(self):
        return self.token_id

    def natural_key(self):
        return (self.token_id,)