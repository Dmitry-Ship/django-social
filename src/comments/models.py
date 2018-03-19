from django.db import models
from utils.model_behaviors import Deletable, Timestampable, Authorable


class CommentQuerySet(models.QuerySet):
    pass


class CommentManager(models.Manager):
    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db)


class Comment(Deletable, Timestampable, Authorable):
    content = models.TextField(max_length=140, null=False, blank=False)
    objects = CommentManager()
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE,)

    def __str__(self):
        return str(self.content)