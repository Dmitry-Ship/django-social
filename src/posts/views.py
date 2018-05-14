from itertools import chain
from rest_framework import permissions
from .serializers import PostSerializer
from .models import Post
from follows.models import Follow
from utils import mixins as custom_mixins, permissions as custom_permissions, decorators, responses
from rest_framework import generics


@responses.successful_response_decorator
class PostsAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'author'

    @decorators.require_parameter('user')
    def get_queryset(self, query):
        return Post.active.filter(author=query)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


@responses.successful_response_decorator
class PostItemAPIView(generics.RetrieveUpdateDestroyAPIView, custom_mixins.DestroyModelMixin):
    queryset = Post.active.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, custom_permissions.IsOwnerOrReadOnly]


@responses.successful_response_decorator
class FeedAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        users = Follow.active.filter(from_person=self.request.user.id).values_list('to_person')
        qs = Post.active.filter(author__in=chain(users, [self.request.user]))

        return qs.order_by('-create_date')


@responses.successful_response_decorator
class MyPostsAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Post.active.filter(author=self.request.user)

        return qs.order_by('-create_date')
