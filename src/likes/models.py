from django.db import models
from utils.model_behaviors import Deletable, Timestampable, Authorable
from django.dispatch import receiver
from django.db.models.signals import pre_save
import likes.errors as errors


class PostLike(Deletable, Timestampable, Authorable):
    target = models.ForeignKey('posts.Post', on_delete=models.CASCADE)


class CommentLike(Deletable, Timestampable, Authorable):
    target = models.ForeignKey('comments.PostComment', on_delete=models.CASCADE)


@receiver(pre_save, sender=CommentLike)
def create_comment_like(sender, instance, *args, **kwargs):
    if not instance.pk:
        if CommentLike.active.filter(target=instance.comment, author=instance.author).exists():
            raise errors.AlreadyLiked()


@receiver(pre_save, sender=PostLike)
def create_post_like(sender, instance, *args, **kwargs):
    if not instance.pk:
        if PostLike.active.filter(target=instance.post, author=instance.author).exists():
            raise errors.AlreadyLiked()
