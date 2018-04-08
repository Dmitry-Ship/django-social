from rest_framework import generics, permissions
from .serializers import LikeSerializer
from .models import Like, Target
from utils import mixins as custom_mixins, permissions as custom_permissions, decorators
from .decorators import handle_likes_errors


class LikesAPIView(generics.ListCreateAPIView, custom_mixins.CreateModelMixin, custom_mixins.ListModelMixin):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Like.active.all()

        target = self.request.query_params.get('target', None)
        if target is not None:
            qs = qs.filter(target=target)

        user = self.request.query_params.get('user', None)
        if user is not None:
            qs = qs.filter(author=user)
        return qs

    @handle_likes_errors
    @decorators.custom_404
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

