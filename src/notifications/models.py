from django.db import models
from utils.model_behaviors import Deletable, Timestampable, Authorable
from django.conf import settings
from .constans import TYPE_CHOICES


class Notification(Deletable, Timestampable, Authorable):
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, null=False)


class NotificationChild(Notification):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE, primary_key=True, parent_link=True,)

    class Meta:
        abstract = True


class NotificationPostLiked(NotificationChild):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)


class NotificationPostCommented(NotificationChild):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    comment = models.ForeignKey('comments.PostComment', on_delete=models.CASCADE)


class NotificationCommentLiked(NotificationChild):
    comment = models.ForeignKey('comments.PostComment', on_delete=models.CASCADE)


class NotificationFollowed(NotificationChild):
    pass
