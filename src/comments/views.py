from django.db.models import Q
from rest_framework import generics, permissions
from .serializers import CommentSerializer
from .models import Comment
from utils import mixins as custom_mixins, permissions as custom_permissions, decorators
from posts.models import Post


class CommentsAPIView(generics.ListCreateAPIView, custom_mixins.CreateModelMixin, custom_mixins.ListModelMixin):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Comment.active.all()

        query = self.request.GET.get('q', )
        if query is not None:
            qs = qs.filter(Q(content__icontains=query)).distinct()

        user = self.request.query_params.get('user', None)
        if user is not None:
            qs = qs.filter(author=user)

        post = self.request.query_params.get('post', None)
        if post is not None:
            qs = qs.filter(post=post)

        return qs

    @decorators.custom_404
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