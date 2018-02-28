from django.db import models
from django.contrib.auth.models import User
from utils.model_behaviors import Timestampable, Deletable


class Follow(Timestampable, Deletable):
    from_person = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='from_people')
    to_person = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='to_people')


    class Meta:
        unique_together = ('from_person', 'to_person')
