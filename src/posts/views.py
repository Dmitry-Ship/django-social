from django.db.models import Q
from rest_framework import generics, mixins, permissions
from .serializers import PostSerializer
from .models import Post
from utils.permissions import IsOwnerOrReadOnly


class PostsAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Post.objects.all()
        query = self.request.GET.get('q', )
        if query is not None:
            qs = qs.filter(Q(content__icontains=query)).distinct()
        return qs

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostItemAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticated]


