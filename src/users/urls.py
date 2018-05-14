from django.urls import path
from .views import UserProfilesAPIView, UserProfileItemAPIView, MeAPIView, MeUpdateAPIView


urlpatterns = [
    path('', UserProfilesAPIView.as_view()),
    path('<int:pk>', UserProfileItemAPIView.as_view()),
    path('me', MeAPIView.as_view()),
    path('updateMe', MeUpdateAPIView.as_view()),
]