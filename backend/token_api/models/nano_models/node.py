from django.db import models

from ..token_models.application import Application

class NodeManager(models.Manager):
    def get_by_natural_key(self, node_id):
        return self.get(node_id=node_id)


class Node(models.Model):
    URL = models.CharField(max_length=512)

    node_id = models.CharField(max_length=256, default=None)

    application = models.ForeignKey(Application, related_name="node_application", on_delete=models.PROTECT)

    objects = NodeManager()

    def __str__(self):
        return u'%s' % (self.URL)

    def natural_key(self):
        return (self.node_id,)