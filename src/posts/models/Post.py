from django.db import models
from utils.model_behaviors import Deletable, Timestampable, Authorable
from comments.models import Comment
from likes.models import Like, Target
import likes.errors as errors
from django.core.exceptions import ObjectDoesNotExist
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

    def comment(self, user, text):
        obj = Comment.active.create(author=user, post=self, content=text)
        return obj

    def like(self, user):
        obj = Like.active.create(author=user, target=self.target)
        return obj

    @property
    def likes(self):
        qs = Like.active.filter(target=self.target)
        return qs

    def dislike(self, user):
        try:
            obj = Like.active.get(target=self.target, author=user)
            obj.deactivate()
            obj.save()
            return obj
        except ObjectDoesNotExist:
            raise errors.NeverLiked()

    def __str__(self):
        return str(self.content)


@receiver(pre_save, sender=Post)
def create_post_target(sender, instance, raw, **kwargs):
    if hasattr(instance, 'target') is False:
        target = Target.objects.create()
        instance.target = target
