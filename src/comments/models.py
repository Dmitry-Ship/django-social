from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from entities.models import Entity
from entities.constants import COMMENT
from likes.behaviors import Likable
from utils.model_behaviors import Deletable, Timestampable, Authorable


class Comment(Deletable, Timestampable, Authorable, Likable):
    id = models.OneToOneField(Entity, on_delete=models.CASCADE, primary_key=True)
    content = models.TextField(max_length=140, null=False, blank=False)
    target_entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='target_entity')

    def __str__(self):
        return str(self.content)


@receiver(pre_save, sender=Comment)
def create_comment_target(sender, instance, raw, **kwargs):
    if hasattr(instance, 'id') is False:
        entity = Entity.objects.create(type=COMMENT)
        instance.id = entity