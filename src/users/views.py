from rest_framework import generics, permissions
from rest_framework.views import APIView
from .serializers import UserProfileDetailSerializer, UserProfileListSerializer
from django.contrib.auth.models import User
from utils import responses, mixins as custom_mixins
from utils.decorators import custom_404
from .decorators import handle_follow_errors
from .models import Follow


class UserProfilesAPIView(generics.ListCreateAPIView, custom_mixins.ListModelMixin, custom_mixins.CreateModelMixin):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileListSerializer


class UserProfileItemAPIView(generics.RetrieveAPIView, custom_mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileDetailSerializer


class FollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    @custom_404
    @handle_follow_errors
    def post(request, pk):
        user = User.objects.get(pk=request.user.id)
        target = User.objects.get(pk=pk)
        Follow.objects.create(to_person=target, from_person=user)

        return responses.successful_response()


class UnfollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    @custom_404
    @handle_follow_errors
    def post(request, pk):
        user = User.objects.get(pk=request.user.id)
        target = User.objects.get(pk=pk)
        follow = Follow.active.get(to_person=target, from_person=user)
        follow.deactivate()
        follow.save()

        return responses.successful_response()