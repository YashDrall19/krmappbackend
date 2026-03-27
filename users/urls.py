from . import views
from django.urls import path

urlpatterns = [
    path("home", views.home),
    path("adduser", views.create_user),
    path("getuser", views.get_users),
]