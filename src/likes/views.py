from rest_framework import generics, permissions
from .serializers import LikeSerializer
from .models import Like
from utils import mixins as custom_mixins, permissions as custom_permissions


class LikesAPIView(generics.ListCreateAPIView, custom_mixins.CreateModelMixin, custom_mixins.ListModelMixin):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Like.active.all()

        post = self.request.query_params.get('post', None)
        if post is not None:
            qs = qs.filter(entity=post)
        return qs

        user = self.request.query_params.get('user', None)
        if user is not None:
            qs = qs.filter(author=user)
        return qs

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class LikeItemAPIView(
                        custom_mixins.RetrieveModelMixin,
                        custom_mixins.DestroyModelMixin,
                        custom_mixins.UpdateModelMixin,
                        generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = Like.active.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated, custom_permissions.IsOwnerOrReadOnly]

