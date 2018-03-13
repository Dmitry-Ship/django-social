from django.urls import path
from .views import UserProfilesAPIView, FollowAPIView, UserProfileItemAPIView, UnfollowAPIView


urlpatterns = [
    path('', UserProfilesAPIView.as_view()),
    path('<int:pk>', UserProfileItemAPIView.as_view()),
    path('follow/<int:pk>', FollowAPIView.as_view()),
    path('unfollow/<int:pk>', UnfollowAPIView.as_view()),
]