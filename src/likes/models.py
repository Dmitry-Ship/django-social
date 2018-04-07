from django.db import models
from utils.model_behaviors import Deletable, Timestampable, Authorable
from django.dispatch import receiver
from django.db.models.signals import pre_save
import likes.errors as errors


class LikeQuerySet(models.QuerySet):
    pass


class LikeManager(models.Manager):
    def get_queryset(self):
        return LikeQuerySet(self.model, using=self._db)


class Target(models.Model):
    pass


def get_target():
    return Target.objects.get_or_create()[1].id


class Like(Deletable, Timestampable, Authorable):
    objects = LikeManager()
    target = models.ForeignKey(Target, on_delete=models.CASCADE, default=get_target)


@receiver(pre_save, sender=Like)
def create_like(sender, instance, *args, **kwargs):
    if not instance.pk:
        if Like.active.filter(target=instance.target, author=instance.author).exists():
            raise errors.AlreadyLiked()