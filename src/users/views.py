from rest_framework import generics, mixins, permissions
from .serializers import UserProfileSerializer
from .models import UserProfile
from django.contrib.auth.models import User


class UserProfilesAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = User.objects.all()
        return qs

    def perform_create(self, serializer):
        return serializer.save()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
