from django.urls import path

from . import views

app_name = 'encyclopedia'

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:article>", views.article, name="article"),
    path("search/", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("edit/<str:article>", views.edit, name="edit"),
    path("random_article/", views.randompage, name="ranom_article"),

]
