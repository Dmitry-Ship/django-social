from django.urls import path
from .views import LikesAPIView

urlpatterns = [
    path('', LikesAPIView.as_view()),
]