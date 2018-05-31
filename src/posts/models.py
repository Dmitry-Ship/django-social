from django.db import models
from django.db.models import Count
from utils.model_behaviors import Deletable, Timestampable, Authorable
from likes.models import PostLike
from likes.behaviors import likable
from comments.models import PostComment
from comments.behaviors import commentable


class PostQuerySet(models.QuerySet):
    def popular(self):
        return self.objects.annotate(num_likes=Count('likes')).filter(num_likes__gte=2)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def popular(self):
        return self.get_queryset().popular()


class Post(Deletable, Timestampable, Authorable, likable(model=PostLike), commentable(model=PostComment)):
    content = models.CharField(max_length=140, null=False, blank=False)
    objects = PostManager()

    def __str__(self):
        return str(self.content)


# @receiver(pre_save, sender=Post)
# def create_post_target(sender, instance, raw, **kwargs):
#     if hasattr(instance, 'id') is False:
#         entity = Entity.objects.create(type=POST)
#         instance.id = entity
