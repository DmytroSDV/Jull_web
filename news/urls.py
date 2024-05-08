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
    path("usds/", views.all_banks_usd, name="all_banks_usd"),
    path("eurs/", views.all_banks_eur, name="all_banks_eur"),
    path("weather/", views.all_weather_cities, name="all_weather_cities"),
    path("weather/details", views.all_weather_details, name="all_weather_details"),
]
