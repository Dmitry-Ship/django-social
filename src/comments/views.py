from django.shortcuts import get_object_or_404
from rest_framework import permissions
from .serializers import CommentSerializer
from .models import PostComment
from posts.models import Post
from utils import mixins as custom_mixins, permissions as custom_permissions, decorators, responses
from rest_framework import generics


@responses.successful_response_decorator
class CommentsAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.require_parameter('post')
    def get_queryset(self, query):
        return PostComment.active.filter(target=query)

    def perform_create(self, serializer):
        post_id = self.request.data['post']
        post = get_object_or_404(Post, pk=post_id)

        return serializer.save(author=self.request.user, target=post)


@responses.successful_response_decorator
class CommentItemAPIView(generics.RetrieveUpdateDestroyAPIView, custom_mixins.DestroyModelMixin):
    queryset = PostComment.active.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, custom_permissions.IsOwnerOrReadOnly]