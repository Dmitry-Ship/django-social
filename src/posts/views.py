from django.db.models import Q
from rest_framework import generics, permissions
from .serializers import PostSerializer
from .models import Post
from utils import mixins as custom_mixins, permissions as custom_permissions


class PostsAPIView(generics.ListCreateAPIView, custom_mixins.CreateModelMixin, custom_mixins.ListModelMixin):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Post.active.all()

        query = self.request.GET.get('q', )
        if query is not None:
            qs = qs.filter(Q(content__icontains=query)).distinct()

        user = self.request.query_params.get('user', None)
        if user is not None:
            qs = qs.filter(author=user)
        return qs

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

