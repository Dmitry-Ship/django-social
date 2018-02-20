from django.db import models
import datetime
from django.utils import timezone
from utils.model_behaviors import Deletable, Timestampable, Authorable


class PostQuerySet(models.QuerySet):
    pass
    # def recent(self):
    #     time = timezone.now() - datetime.timedelta(days=1)
    #     return self.filter(timestamp__gte=time)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    # def recent(self):
    #     return self.get_queryset().recent()


class Post(Deletable, Timestampable, Authorable):
    content = models.CharField(max_length=140, null=True, blank=True)
    objects = PostManager()

    def __str__(self):
        return str(self.content)