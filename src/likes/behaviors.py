from .models import Like


class Likable:
    @property
    def likes(self):
        qs = Like.active.filter(target_entity=self.id)
        return qs
