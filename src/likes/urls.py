from django.urls import path
from .views import LikesAPIView, MyLikedCommentsAPIView, MyLikedPostsAPIView

urlpatterns = [
    path('', LikesAPIView.as_view()),
    path('/myLikedPosts', MyLikedPostsAPIView.as_view()),
    path('/myLikedComments', MyLikedCommentsAPIView.as_view()),
]