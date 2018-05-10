from django.urls import path
from .views import PostItemAPIView, PostsAPIView, MyPostsAPIView

urlpatterns = [
    path('', PostsAPIView.as_view()),
    path('<int:pk>', PostItemAPIView.as_view()),
    path('/myPosts', MyPostsAPIView.as_view()),
]