from django.urls import path

from accountant.views import (
    home_view,
    list_student_view,
    password_change_view,
    pay_fee_view,
    profile_update_view,
    profile_view,
)

app_name = "accountant"

urlpatterns = [
    path("", home_view, name="home"),
    path("students/", list_student_view, name="list-student"),
    path("pay-fee/<uuid>/", pay_fee_view, name="pay-fee"),
    # Profile Views
    path("profile/", profile_view, name="profile"),
    path("profile_update/", profile_update_view, name="profile-update"),
    path("password_change/", password_change_view, name="password-change"),
]
