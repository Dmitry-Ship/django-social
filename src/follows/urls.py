from django.urls import path
from .views import FollowAPIView, UnfollowAPIView


urlpatterns = [
    path('follow', FollowAPIView.as_view()),
    path('unfollow', UnfollowAPIView.as_view()),
]