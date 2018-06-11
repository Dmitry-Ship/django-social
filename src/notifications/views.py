from rest_framework import permissions
from rest_framework import generics
from .serializers import (NotificationPostLikedSerializer, NotificationCommentLikedSerializer,
                        NotificationPostCommentedSerializer, NotificationFollowedSerializer)
from .models import NotificationPostLiked, NotificationCommentLiked, NotificationPostCommented, NotificationFollowed
from utils.responses import successful_response


def get_serializer_data(model, serializer_class, request):
    qs = model.objects.filter(notification__receiver=request.user)
    serializer = serializer_class(qs, many=True)
    return serializer.data


class NotificationsAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        post_liked = get_serializer_data(NotificationPostLiked, NotificationPostLikedSerializer, request)
        comment_liked = get_serializer_data(NotificationCommentLiked, NotificationCommentLikedSerializer, request)
        post_commented = get_serializer_data(NotificationPostCommented, NotificationPostCommentedSerializer, request)
        followed = get_serializer_data(NotificationFollowed, NotificationFollowedSerializer, request)

        return successful_response(data=post_liked + comment_liked + post_commented + followed)


