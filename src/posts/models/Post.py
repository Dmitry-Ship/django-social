from django.db import models
from utils.model_behaviors import Deletable, Timestampable, Authorable
from comments.models import Comment


class PostQuerySet(models.QuerySet):
    pass
    # def recent(self):
    #     time = timezone.now() - datetime.timedelta(days=1)
    #     return self.filter(timestamp__gte=time)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    # def recent(self):
    #     return self.get_queryset().recent()


class Post(Deletable, Timestampable, Authorable):
    content = models.CharField(max_length=140, null=False, blank=False)
    objects = PostManager()

    @property
    def comments(self):
        qs = Comment.active.filter(post=self.id)
        return qs

    def comment(self, user, text):
        obj = Comment.active.create(author=user, post=self, content=text)
        return obj

    def __str__(self):
        return str(self.content)