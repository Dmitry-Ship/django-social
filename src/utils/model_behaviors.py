from django.db import models
from django.contrib.auth.models import User


class Deletable(models.Model):
    is_deleted = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    class Meta:
        abstract = True


class Timestampable(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Authorable(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True