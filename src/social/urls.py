from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.views import signup
from posts.views import FeedAPIView
from notifications.views import NotificationsAPIView

urlpatterns = [
    path('feed/', FeedAPIView.as_view()),
    path('notifications/', NotificationsAPIView.as_view()),
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
    path('comments/', include('comments.urls')),
    path('likes/', include('likes.urls')),
    path('follows/', include('follows.urls')),
    path('users/', include('users.urls')),
    path('accounts/login', auth_views.LoginView.as_view()),
    path('accounts/logout', auth_views.LogoutView.as_view()),
    path('signup', signup),
]
