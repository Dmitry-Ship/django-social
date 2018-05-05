from django.db import models
from django.conf import settings
import datetime


class DeletableQuerySet(models.QuerySet):
    pass


class DeletableManager(models.Manager):
    def get_queryset(self):
        return DeletableQuerySet(self.model, using=self._db).filter(is_deleted=False)


class Deletable(models.Model):
    is_deleted = models.BooleanField(default=False)
    objects = models.Manager()
    active = DeletableManager()

    def deactivate(self):
        self.is_deleted = True
        self.save()

    class Meta:
        abstract = True


class Timestampable(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk:
            self.modified_date = datetime.datetime.utcnow()
        super(Timestampable, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Authorable(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True
