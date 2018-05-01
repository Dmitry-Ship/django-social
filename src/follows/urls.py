from django.urls import path
from .views import FollowAPIView, UnfollowAPIView, FollowersAPIView, FollowingAPIView


urlpatterns = [
    path('follow', FollowAPIView.as_view()),
    path('unfollow', UnfollowAPIView.as_view()),
    path('followers', FollowersAPIView.as_view()),
    path('following', FollowingAPIView.as_view()),
]