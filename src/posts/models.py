from django.db import models
from django.db.models.signals import pre_save
from django.db.models import Count
from django.dispatch import receiver
from utils.model_behaviors import Deletable, Timestampable, Authorable
from comments.behaviors import Commentable
from likes.behaviors import Likable
from entities.constants import POST
from entities.models import Entity


class PostQuerySet(models.QuerySet):
    def popular(self):
        return self.objects.annotate(num_likes=Count('likes')).filter(num_likes__gte=2)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def popular(self):
        return self.get_queryset().popular()


class Post(Deletable, Timestampable, Authorable, Likable, Commentable):
    id = models.OneToOneField(Entity, on_delete=models.CASCADE, primary_key=True)
    content = models.CharField(max_length=140, null=False, blank=False)
    objects = PostManager()

    def __str__(self):
        return str(self.content)


@receiver(pre_save, sender=Post)
def create_post_target(sender, instance, raw, **kwargs):
    if hasattr(instance, 'id') is False:
        entity = Entity.objects.create(type=POST)
        instance.id = entity
