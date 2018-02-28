from rest_framework import generics, mixins, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserProfileDetailSerializer, UserProfileListSerializer, FollowSerializer
from .models import UserProfile, Follow
from django.contrib.auth.models import User


class UserProfilesAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    queryset = User.objects.all()
    serializer_class = UserProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserProfileItemAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):

        user = User.objects.get(pk=pk)
        serializer = UserProfileDetailSerializer(user)

        return Response({'status': True, 'data': serializer.data})


class FollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = User.objects.get(pk=request.user.id)
        target = User.objects.get(pk=pk).userprofile

        user.userprofile.follow(target=target)

        return Response({'status': True})


class UnfollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = User.objects.get(pk=request.user.id)
        target = User.objects.get(pk=pk).userprofile

        user.userprofile.unfollow(target=target)

        return Response({'status': True})