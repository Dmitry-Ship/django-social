from django.db import models
from utils.model_behaviors import Deletable, Timestampable, Authorable
from comments.models import Comment
from likes.models import Like, Target
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db.models import Count


class PostQuerySet(models.QuerySet):
    def popular(self):
        return self.objects.annotate(num_likes=Count('likes')).filter(num_likes__gte=2)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def popular(self):
        return self.get_queryset().popular()


class Post(Deletable, Timestampable, Authorable):
    content = models.CharField(max_length=140, null=False, blank=False)
    objects = PostManager()
    target = models.OneToOneField(Target, on_delete=models.CASCADE)

    @property
    def comments(self):
        qs = Comment.active.filter(post=self.id)
        return qs

    @property
    def likes(self):
        qs = Like.active.filter(target=self.target)
        return qs

    def __str__(self):
        return str(self.content)


@receiver(pre_save, sender=Post)
def create_post_target(sender, instance, raw, **kwargs):
    if hasattr(instance, 'target') is False:
        target = Target.objects.create()
        instance.target = target