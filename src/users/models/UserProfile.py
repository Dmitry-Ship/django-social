from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from ..constants import GENDER_CHOICES
from utils.model_behaviors import Timestampable
from follows.models import Follow


class UserProfile(Timestampable):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True, on_delete=models.CASCADE)
    phone_number = models.CharField(blank=True, null=True, max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,)

    @property
    def followers(self):
        qs = Follow.active.filter(to_person=self.user).values_list('from_person', flat=True)
        return qs

    @property
    def following(self):
        qs = Follow.active.filter(from_person=self.user).values_list('to_person', flat=True)
        return qs

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def full_name(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    def __str__(self):
        return self.full_name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_userprofile(sender, instance, **kwargs):
    instance.userprofile.save()