from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:article_name>", views.article, name="article"),
    path("new", views.new_article, name="new_article"),
    path("random", views.random_article, name="random_article"),
    path("wiki/<str:article_name>/edit",
         views.edit_article, name="edit_article"),

]
