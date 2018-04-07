from django.urls import path
from .views import LikeItemAPIView, LikesAPIView

urlpatterns = [
    path('', LikesAPIView.as_view()),
    path('<int:pk>', LikeItemAPIView.as_view()),
]