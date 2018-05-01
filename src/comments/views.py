from rest_framework import generics, permissions
from .serializers import CommentSerializer
from .models import Comment
from utils import mixins as custom_mixins, permissions as custom_permissions, decorators
from posts.models import Post


class CommentsAPIView(generics.ListCreateAPIView, custom_mixins.CreateModelMixin, custom_mixins.ListModelMixin):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.require_parameter('post')
    def get_queryset(self, query):
        return Comment.active.filter(post=query)

    @decorators.handle_404
    def perform_create(self, serializer):
        post_id = self.request.data['post']
        post = Post.active.get(pk=post_id)

        return serializer.save(author=self.request.user, post=post)


class CommentItemAPIView(
                        custom_mixins.RetrieveModelMixin,
                        custom_mixins.DestroyModelMixin,
                        custom_mixins.UpdateModelMixin,
                        generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = Comment.active.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, custom_permissions.IsOwnerOrReadOnly]