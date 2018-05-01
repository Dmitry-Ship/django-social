from itertools import chain
from rest_framework import generics, permissions
from .serializers import PostSerializer
from .models import Post
from follows.models import Follow
from utils import mixins as custom_mixins, permissions as custom_permissions, decorators


class PostsAPIView(generics.ListCreateAPIView, custom_mixins.CreateModelMixin, custom_mixins.ListModelMixin):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.require_parameter('user')
    def get_queryset(self, query):
        return Post.active.filter(author=query)


    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class PostItemAPIView(
                        custom_mixins.RetrieveModelMixin,
                        custom_mixins.DestroyModelMixin,
                        custom_mixins.UpdateModelMixin,
                        generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = Post.active.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, custom_permissions.IsOwnerOrReadOnly]


class FeedAPIView(generics.ListAPIView, custom_mixins.ListModelMixin):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        users = Follow.active.filter(from_person=self.request.user.id).values_list('to_person')
        qs = Post.active.filter(author__in=chain(users, [self.request.user]))

        return qs.order_by('-create_date')


class MyPostsAPIView(generics.ListAPIView, custom_mixins.ListModelMixin):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Post.active.filter(author=self.request.user)

        return qs.order_by('-create_date')
