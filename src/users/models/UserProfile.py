from django.db import models
from django.contrib.auth.models import User
from constants import GENDER_CHOICES
from utils.model_behaviors import Timestampable
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from .Follow import Follow
from users import errors


class UserProfile(Timestampable):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
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

    def follow(self, target):
        obj = Follow.active.create(from_person=self.user, to_person=target)
        return obj

    def unfollow(self, target):
        try:
            obj = Follow.active.get(from_person=self.user, to_person=target)
            obj.deactivate()
            obj.save()
            return obj
        except ObjectDoesNotExist:
            raise errors.NotFollowing()

    def __str__(self):
        return self.full_name


@receiver(post_save, sender=User)
def create_user_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_userprofile(sender, instance, **kwargs):
    instance.userprofile.save()