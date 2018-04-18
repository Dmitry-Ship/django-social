from django.urls import path
from .views import UserProfilesAPIView, UserProfileItemAPIView


urlpatterns = [
    path('', UserProfilesAPIView.as_view()),
    path('<int:pk>', UserProfileItemAPIView.as_view()),
]