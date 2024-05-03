from django.urls import path

from . import views
from users import views as users_views
app_name = "news"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", users_views.loginuser, name="login"),
    path("articles/", views.all_articles, name="all_articles"),
    path("article/<str:title>", views.one_article, name="one_article"),
    path("siences/", views.all_siences, name="all_siences"),
    path("sience/<str:title>", views.one_sience, name="one_sience"),
    path("technos/", views.all_technos, name="all_technos"),
    path("techno/<str:title>", views.one_techno, name="one_techno"),
    path("sports/", views.all_sports, name="all_sports"),
    path("sport/<str:title>", views.one_sport, name="one_sport"),
]
