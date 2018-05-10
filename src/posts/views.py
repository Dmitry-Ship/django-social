from itertools import chain
from rest_framework import permissions
from .serializers import PostSerializer
from .models import Post
from follows.models import Follow
from utils import generics as custom_generics, permissions as custom_permissions, decorators


class PostsAPIView(custom_generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.require_parameter('user')
    def get_queryset(self, query):
        return Post.active.filter(author=query)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class PostItemAPIView(custom_generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.active.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, custom_permissions.IsOwnerOrReadOnly]


class FeedAPIView(custom_generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        users = Follow.active.filter(from_person=self.request.user.id).values_list('to_person')
        qs = Post.active.filter(author__in=chain(users, [self.request.user]))

        return qs.order_by('-create_date')


class MyPostsAPIView(custom_generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Post.active.filter(author=self.request.user)

        return qs.order_by('-create_date')
