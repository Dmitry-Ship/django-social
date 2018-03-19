from django.urls import path
from .views import PostItemAPIView, PostsAPIView, CommentAPIView

urlpatterns = [
    path('', PostsAPIView.as_view()),
    path('<int:pk>', PostItemAPIView.as_view()),
    path('<int:pk>/comment', CommentAPIView.as_view()),
]