from rest_framework import permissions
from .serializers import LikeSerializer
from posts.serializers import PostSerializer
from .models import Like
from entities.models import Entity
from utils import generics as custom_generics, decorators
from .decorators import handle_likes_errors
from posts.models import Post


class LikesAPIView(custom_generics.ListCreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    @decorators.require_parameter('entity')
    def get_queryset(query):
        return Like.active.filter(target_entity=query)

    @handle_likes_errors
    @decorators.handle_404
    def perform_create(self, serializer):
        entity_id = self.request.data['entity']
        entity = Entity.objects.get(pk=entity_id)

        return serializer.save(author=self.request.user, target_entity=entity)


class MyLikesAPIView(custom_generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        targets = Like.active.filter(author=self.request.user).values_list('target_entity')
        return Post.active.filter(id__in=targets)

