from . import views
from django.urls import path

urlpatterns = [
    path("home", views.home),
    path("adduser", views.create_user),
    path("getuser", views.get_users),
    path("login", views.login),
    path("auth/google", views.google_login),
]