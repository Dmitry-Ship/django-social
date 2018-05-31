from django.db import models
from likes.models import CommentLike
from utils.model_behaviors import Deletable, Timestampable, Authorable
from likes.behaviors import likable


class PostComment(Deletable, Timestampable, Authorable, likable(model=CommentLike)):
    content = models.TextField(max_length=140, null=False, blank=False)
    target = models.ForeignKey('posts.Post', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.content)
