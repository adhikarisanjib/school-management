from django.urls import path

from base.views import (
    email_verify_view,
    home_view,
    login_view,
    logout_view,
    password_change_view,
    password_reset_request_view,
    password_reset_view,
    register_view,
    user_deactivate_view,
    user_delete_view,
    user_profile_view,
    user_update_view,
)

app_name = "base"

urlpatterns = [
    path("", home_view, name="home"),
    path("register/", register_view, name="user-register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("user_profile/", user_profile_view, name="user-profile"),
    path("user_profile/<str:user_id>", user_profile_view, name="user-profile"),
    path("user_update/", user_update_view, name="user-update"),
    path("email_verification/<uidb64>/<token>/", email_verify_view, name="email-verify"),
    path("password_change/", password_change_view, name="password-change"),
    path("password_reset_request/", password_reset_request_view, name="password-reset-request"),
    path("password_reset/<uidb64>/<token>/", password_reset_view, name="password-reset"),
    path("user_deactivate/", user_deactivate_view, name="user-deactivate"),
    path("user_delete/", user_delete_view, name="user-delete"),
]
