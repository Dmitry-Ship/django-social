from django.db import models
from utils.model_behaviors import Deletable, Timestampable, Authorable
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
import likes.errors as errors
from notifications.models import NotificationPostLiked, NotificationCommentLiked
from notifications.constans import POST_LIKED, COMMENT_LIKED


class PostLike(Deletable, Timestampable, Authorable):
    target = models.ForeignKey('posts.Post', on_delete=models.CASCADE)


class CommentLike(Deletable, Timestampable, Authorable):
    target = models.ForeignKey('comments.PostComment', on_delete=models.CASCADE)


@receiver(pre_save, sender=CommentLike)
def create_comment_like(sender, instance, *args, **kwargs):
    if not instance.pk:
        if CommentLike.active.filter(target=instance.target, author=instance.author).exists():
            raise errors.AlreadyLiked()


@receiver(pre_save, sender=PostLike)
def create_post_like(sender, instance, *args, **kwargs):
    if not instance.pk:
        if PostLike.active.filter(target=instance.target, author=instance.author).exists():
            raise errors.AlreadyLiked()


@receiver(post_save, sender=PostLike)
def create_post_liked_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.target
        author = instance.author

        notification_liked = NotificationPostLiked(author=author, receiver=post.author, type=POST_LIKED, post=post)
        notification_liked.save()


@receiver(post_save, sender=CommentLike)
def create_comment_liked_notification(sender, instance, created, **kwargs):
    if created:
        comment = instance.target
        author = instance.author

        notification_liked = NotificationCommentLiked(author=author, receiver=comment.author, type=COMMENT_LIKED, comment=comment)
        notification_liked.save()
