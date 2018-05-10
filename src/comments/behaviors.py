from .models import Comment


class Commentable:
    @property
    def comments(self):
        return Comment.active.filter(target_entity=self.id)
