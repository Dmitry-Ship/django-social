from rest_framework import generics, permissions
from .serializers import LikeSerializer
from posts.serializers import PostSerializer
from .models import Like, Target
from utils import mixins as custom_mixins, permissions as custom_permissions, decorators
from .decorators import handle_likes_errors
from posts.models import Post


class LikesAPIView(generics.ListCreateAPIView, custom_mixins.CreateModelMixin, custom_mixins.ListModelMixin):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.require_parameter('target')
    def get_queryset(self, query):
        return Like.active.filter(target=query)

    @handle_likes_errors
    @decorators.handle_404
    def perform_create(self, serializer):
        target_id = self.request.data['target']
        target = Target.objects.get(pk=target_id)

        return serializer.save(author=self.request.user, target=target)


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
        targets = Like.active.filter(author=self.request.user).values_list('target')
        return Post.active.filter(target__in=targets)

