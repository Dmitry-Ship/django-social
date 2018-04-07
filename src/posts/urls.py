from django.urls import path
from .views import PostItemAPIView, PostsAPIView, CommentAPIView, LikeAPIView, DislikeAPIView

urlpatterns = [
    path('', PostsAPIView.as_view()),
    path('<int:pk>', PostItemAPIView.as_view()),
    path('<int:pk>/comment', CommentAPIView.as_view()),
    path('<int:pk>/like', LikeAPIView.as_view()),
    path('<int:pk>/dislike', DislikeAPIView.as_view()),
]