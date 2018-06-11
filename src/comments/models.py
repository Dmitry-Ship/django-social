from likes.models import CommentLike
from likes.behaviors import likable

from django.db import models
from utils.model_behaviors import Deletable, Timestampable, Authorable
from django.dispatch import receiver
from django.db.models.signals import post_save
from notifications.models import NotificationPostCommented
from notifications.constans import POST_COMMENTED


class PostComment(Deletable, Timestampable, Authorable, likable(model=CommentLike)):
    content = models.TextField(max_length=140, null=False, blank=False)
    target = models.ForeignKey('posts.Post', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.content)


@receiver(post_save, sender=PostComment)
def create_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.target
        author = instance.author

        notification_liked = NotificationPostCommented(author=author, receiver=post.author, type=POST_COMMENTED, comment=instance, post=post)
        notification_liked.save()