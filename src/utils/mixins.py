from rest_framework import mixins


class DestroyModelMixin(mixins.DestroyModelMixin):
    def perform_destroy(self, instance):
        instance.deactivate()
