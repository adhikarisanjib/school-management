from django.urls import path

from website.views import home_view, login_view, logout_view

app_name = "website"


urlpatterns = [
    path("", home_view, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
