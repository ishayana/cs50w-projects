
from django.urls import path

from . import views

app_name = 'network'

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("like/<int:post_id>", views.post_like, name="like"),
    path("<int:user_id>", views.userpage, name="user_page"),
    path("follow/<int:user_id>", views.follow_user, name="follow"),
    path("edit/<int:post_id>", views.edit_post, name="edit_post"),
    path("following/", views.following_posts, name="following_posts"),

]
