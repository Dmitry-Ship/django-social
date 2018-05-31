def likable(model):
    class Likable:
        def __init__(self):
            self.like_model = model

        @property
        def likes(self):
            qs = self.like_model.active.filter(target=self.id)
            return qs

    return Likable
