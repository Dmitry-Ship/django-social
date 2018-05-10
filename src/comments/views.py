from rest_framework import permissions
from .serializers import CommentSerializer
from .models import Comment
from utils import permissions as custom_permissions, generics as custom_generics, decorators
from entities.models import Entity


class CommentsAPIView(custom_generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    @decorators.require_parameter('post')
    def get_queryset(query):
        return Comment.active.filter(post=query)

    @decorators.handle_404
    def perform_create(self, serializer):
        post_id = self.request.data['post']
        post = Entity.objects.get(pk=post_id)

        return serializer.save(author=self.request.user, target_entity=post)


class CommentItemAPIView(custom_generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.active.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, custom_permissions.IsOwnerOrReadOnly]