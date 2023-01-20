from django.urls import path

from conference.views import (
    create_member_view,
    delete_member_view,
    get_member_view,
    get_token_view,
    home_view,
    join_room_view,
    room_view,
)

app_name = "conference"

urlpatterns = [
    path("", home_view, name="home"),
    path("room/", room_view, name="room"),
    path("join_room/<channel>/", join_room_view, name="join-room"),
    path("get_token/", get_token_view, name="get-token"),
    path("create_member/", create_member_view, name="create-member"),
    path("get_member/", get_member_view, name="get-member"),
    path("delete_member/", delete_member_view, name="delete-member"),
]
