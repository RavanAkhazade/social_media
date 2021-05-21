
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:username>", views.user_page, name="user_page"),
    path("following/<str:username>", views.following_page, name="following_page"),
    path("edit/<str:post_id>", views.edit, name="edit"),
    path("postLike/<int:id>", views.like, name="like")
]
