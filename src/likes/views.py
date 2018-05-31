from django.shortcuts import get_object_or_404
from rest_framework import permissions
from .serializers import PostLikeSerializer
from posts.serializers import PostSerializer
from comments.serializers import CommentSerializer
from .models import PostLike, CommentLike
from utils import decorators, responses, mixins
from .decorators import handle_likes_errors
from posts.models import Post
from comments.models import PostComment
from rest_framework import generics


@responses.successful_response_decorator
class PostLikesAPIView(generics.ListCreateAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.require_parameter('post')
    def get_queryset(self, query):
        return PostLike.active.filter(target=query)

    @handle_likes_errors
    def perform_create(self, serializer):
        pos_id = self.request.data['post']
        post = get_object_or_404(Post, pk=pos_id)

        return serializer.save(author=self.request.user, target=post)


@responses.successful_response_decorator
class PostDislikeAPIView(generics.DestroyAPIView, mixins.DestroyModelMixin):
    serializer_class = PostLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        post_id = self.request.data['post']
        like = get_object_or_404(PostLike.active.all(), target=post_id)
        return like


@responses.successful_response_decorator
class MyLikedPostsAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        targets = PostLike.active.filter(author=self.request.user)
        return Post.active.filter(pk__in=targets)


@responses.successful_response_decorator
class MyLikedCommentsAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        targets = CommentLike.active.filter(author=self.request.user)
        return PostComment.active.filter(pk__in=targets)