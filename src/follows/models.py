from django.db import models
from django.contrib.auth.models import User
from utils.model_behaviors import Timestampable, Deletable
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .errors import SelfFollowing


class FollowQuerySet(models.QuerySet):
    def followers(self):
        return self.filter(to_person=self.user).values_list('from_person', flat=True)


class FollowManager(models.Manager):
    def get_queryset(self):
        return FollowQuerySet(self.model, using=self._db)

    def followers(self):
        return self.get_queryset().followers()


class Follow(Timestampable, Deletable):
    from_person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    to_person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target')


@receiver(pre_save, sender=Follow)
def create_follow(sender, instance, *args, **kwargs):
    if not instance.pk:
        if instance.from_person.pk == instance.to_person.pk:
            raise SelfFollowing()