from rest_framework import generics, permissions
from .serializers import LikeSerializer
from posts.serializers import PostSerializer
from .models import Like
from entities.models import Entity
from utils import mixins as custom_mixins, permissions as custom_permissions, decorators
from .decorators import handle_likes_errors
from posts.models import Post


class LikesAPIView(generics.ListCreateAPIView, custom_mixins.CreateModelMixin, custom_mixins.ListModelMixin):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.require_parameter('entity')
    def get_queryset(self, query):
        return Like.active.filter(target_entity=query)

    @handle_likes_errors
    @decorators.handle_404
    def perform_create(self, serializer):
        entity_id = self.request.data['entity']
        entity = Entity.objects.get(pk=entity_id)

        return serializer.save(author=self.request.user, target_entity=entity)


class LikeItemAPIView(
                        custom_mixins.RetrieveModelMixin,
                        custom_mixins.DestroyModelMixin,
                        custom_mixins.UpdateModelMixin,
                        generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = Like.active.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated, custom_permissions.IsOwnerOrReadOnly]


class MyLikesAPIView(generics.ListAPIView, custom_mixins.ListModelMixin):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        targets = Like.active.filter(author=self.request.user).values_list('target_entity')
        return Post.active.filter(id__in=targets)

