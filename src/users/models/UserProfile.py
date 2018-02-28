from django.db import models
from django.contrib.auth.models import User
from constants import GENDER_CHOICES
from utils.model_behaviors import Timestampable
from django.db.models.signals import post_save
from django.dispatch import receiver
from .Follow import Follow


class UserProfile(Timestampable):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    phone_number = models.CharField(blank=True, null=True, max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,)
    following = models.ManyToManyField('self', through=Follow, symmetrical=False, blank=True, related_name='relationships')

    @property
    def followers(self):
        qs = Follow.objects.filter(to_person=self).values_list('from_person', flat=True)
        return qs

    @property
    def full_name(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    def follow(self, target):
        obj, created = Follow.objects.get_or_create(from_person=self, to_person=target)
        return obj

    def unfollow(self, target):
        obj = Follow.objects.get(from_person=self, to_person=target)
        obj.deactivate()
        obj.save()
        return obj

    def __str__(self):
        return self.full_name



@receiver(post_save, sender=User)
def create_user_userprofile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_userprofile(sender, instance, **kwargs):
    instance.userprofile.save()