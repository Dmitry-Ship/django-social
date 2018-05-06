from django.db import models
from .constants import ENTITY_CHOICES


class Entity(models.Model):
    type = models.CharField(
        choices=ENTITY_CHOICES,
        max_length=7
    )


