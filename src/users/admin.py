from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models.User import User

admin.site.register(User, UserAdmin)
