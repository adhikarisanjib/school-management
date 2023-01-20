from django.urls import path

from student.views import (
    home_view,
    password_change_view,
    pay_fee_view,
    post_esewa_failed_view,
    post_esewa_success_view,
    post_khalti_failed_view,
    post_khalti_success_view,
    profile_update_view,
    profile_view,
)

app_name = "student"

urlpatterns = [
    path("", home_view, name="home"),
    path("pay_fee/", pay_fee_view, name="pay-fee"),
    path("post_esewa_success/<pid>/", post_esewa_success_view, name="post-esewa-success"),
    path("post_esewa_failed/", post_esewa_failed_view, name="post-esewa-failed"),
    path("post_khalti_success/", post_khalti_success_view, name="post-khalti-success"),
    path("post_khalti_failed/", post_khalti_failed_view, name="post-khalti-failed"),
    # Profile Views
    path("profile/", profile_view, name="profile"),
    path("profile_update/", profile_update_view, name="profile-update"),
    path("password_change/", password_change_view, name="password-change"),
]
