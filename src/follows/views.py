from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth.models import User
from utils import responses
from utils.decorators import custom_404
from .decorators import handle_follow_errors
from .models import Follow
from django.core.exceptions import ObjectDoesNotExist
from .errors import NotFollowing


class FollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    @custom_404
    @handle_follow_errors
    def post(request):
        user = User.objects.get(pk=request.user.id)
        target = User.objects.get(pk=request.data['user'])
        Follow.objects.create(to_person=target, from_person=user)

        return responses.successful_response()


class UnfollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    @custom_404
    @handle_follow_errors
    def post(request):
        user = User.objects.get(pk=request.user.id)

        target = User.objects.get(pk=request.data['user'])

        try:
            follow = Follow.active.get(to_person=target, from_person=user)
        except ObjectDoesNotExist:
            raise NotFollowing

        follow.deactivate()
        follow.save()

        return responses.successful_response()
