from rest_framework import generics
from utils import mixins as custom_mixins


class ListCreateAPIView(generics.ListCreateAPIView, custom_mixins.CreateModelMixin, custom_mixins.ListModelMixin):
    pass


class RetrieveUpdateDestroyAPIView(
                        custom_mixins.RetrieveModelMixin,
                        custom_mixins.DestroyModelMixin,
                        custom_mixins.UpdateModelMixin,
                        generics.RetrieveUpdateDestroyAPIView):
    pass


class ListAPIView(generics.ListAPIView, custom_mixins.ListModelMixin):
    pass


class RetrieveAPIView(generics.RetrieveAPIView, custom_mixins.RetrieveModelMixin):
    pass


class RetrieveUpdateAPIView(
                        generics.RetrieveUpdateAPIView,
                        custom_mixins.RetrieveModelMixin,
                        custom_mixins.UpdateModelMixin):
    pass


class UpdateAPIView(generics.UpdateAPIView, custom_mixins.UpdateModelMixin):
    pass
