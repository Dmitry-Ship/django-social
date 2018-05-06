from .models import Comment


class Commentable:
    @property
    def comments(self):
        qs = Comment.active.filter(target_entity=self.id)
        return qs