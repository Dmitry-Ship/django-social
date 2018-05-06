from django.db import models
from utils.model_behaviors import Deletable, Timestampable, Authorable
from django.dispatch import receiver
from django.db.models.signals import pre_save
import likes.errors as errors
from entities.models import Entity


class Like(Deletable, Timestampable, Authorable):
    target_entity = models.ForeignKey(Entity, on_delete=models.CASCADE)


@receiver(pre_save, sender=Like)
def create_like(sender, instance, *args, **kwargs):
    if not instance.pk:
        if Like.active.filter(target_entity=instance.target_entity, author=instance.author).exists():
            raise errors.AlreadyLiked()