from django.db import models
from django.conf import settings
from utils.model_behaviors import Timestampable, Deletable
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .errors import SelfFollowing
from notifications.models import NotificationFollowed
from notifications.constans import FOLLOWED


class Follow(Timestampable, Deletable):
    from_person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    to_person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='target')


@receiver(pre_save, sender=Follow)
def create_follow(sender, instance, *args, **kwargs):
    if not instance.pk:
        if instance.from_person.pk == instance.to_person.pk:
            raise SelfFollowing()


@receiver(post_save, sender=Follow)
def create_follow_notification(sender, instance, created, **kwargs):
    if created:
        author = instance.from_person
        notification_receiver = instance.to_person

        notification_liked = NotificationFollowed(author=author, receiver=notification_receiver, type=FOLLOWED)
        notification_liked.save()