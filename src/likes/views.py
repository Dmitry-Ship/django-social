from django.shortcuts import get_object_or_404
from rest_framework import permissions
from .serializers import LikeSerializer
from posts.serializers import PostSerializer
from comments.serializers import CommentSerializer
from .models import Like
from entities.models import Entity
from utils import decorators, responses, mixins
from .decorators import handle_likes_errors
from posts.models import Post
from comments.models import Comment
from rest_framework import generics


@responses.successful_response_decorator
class LikesAPIView(generics.ListCreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.require_parameter('entity')
    def get_queryset(self, query):
        return Like.active.filter(target_entity=query)

    @handle_likes_errors
    def perform_create(self, serializer):
        entity_id = self.request.data['entity']
        entity = get_object_or_404(Entity, pk=entity_id)

        return serializer.save(author=self.request.user, target_entity=entity)


@responses.successful_response_decorator
class DislikeAPIView(generics.DestroyAPIView, mixins.DestroyModelMixin):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        entity_id = self.request.data['entity']
        like = get_object_or_404(Like.active.all(), target_entity_id=entity_id)
        return like


@responses.successful_response_decorator
class MyLikedPostsAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        targets = Like.active.filter(author=self.request.user).values_list('target_entity')
        return Post.active.filter(id__in=targets)


@responses.successful_response_decorator
class MyLikedCommentsAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        targets = Like.active.filter(author=self.request.user).values_list('target_entity')
        return Comment.active.filter(id__in=targets)