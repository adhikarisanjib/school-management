from django.urls import path

from staff.views import (
    home_view,
    password_change_view,
    profile_update_view,
    profile_view,
    take_attendence_view,
)

app_name = "staff"

urlpatterns = [
    path("", home_view, name="home"),
    path("take_attendence/<uuid>/", take_attendence_view, name="take-attendence"),
    # Profile Views
    path("profile/", profile_view, name="profile"),
    path("profile_update/", profile_update_view, name="profile-update"),
    path("password_change/", password_change_view, name="password-change"),
]
