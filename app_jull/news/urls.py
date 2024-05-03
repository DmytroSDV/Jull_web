from django.urls import path

from . import views
from users import views as users_views
app_name = "news"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", users_views.loginuser, name="login"),
]
