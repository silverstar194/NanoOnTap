from django.db import models


class ApplicationManager(models.Manager):
    def get_by_natural_key(self, application_name):
        return self.get(application_name=application_name)


class Application(models.Model):
    application_name = models.CharField(max_length=64, unique=True)

    objects = ApplicationManager()

    class Meta:
        unique_together = [['application_name']]

    def __str__(self):
        return u'%s' % (self.application_name)

    def natural_key(self):
        return (self.application_name,)
