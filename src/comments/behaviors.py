def commentable(model):
    class Commentable:
        def __init__(self):
            self.comment_model = model

        @property
        def comments(self):
            qs = self.comment_model.active.filter(target=self.id)
            return qs

    return Commentable
