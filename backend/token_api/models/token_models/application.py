from django.db import models


class ApplicationManager(models.Manager):
    def get_by_natural_key(self, application_id):
        return self.get(application_id=application_id)


class Application(models.Model):
    application_id = models.CharField(max_length=64, unique=True)

    objects = ApplicationManager()

    class Meta:
        unique_together = [['application_id']]

    def __str__(self):
        return u'%s' % (self.application_id)

    def natural_key(self):
        return (self.application_id,)
