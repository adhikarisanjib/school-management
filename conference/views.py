import json
import random
import time

from agora_token_builder import RtcTokenBuilder
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from conference.models import RoomMember
from school.config import AGORA_APP_CERTIFICATE, AGORA_APP_ID


@login_required
def home_view(request, *args, **kwargs):
    context = {}

    room_members = RoomMember.objects.all()
    if room_members:
        rooms = [room_member.room_name for room_member in room_members]
        rooms = set(rooms)
        context["rooms"] = rooms
    return render(request, "conference/home.html", context)


@login_required
def room_view(request, *args, **kwargs):
    return render(request, "conference/room.html")


@login_required
def join_room_view(request, channel, *args, **kwargs):
    context = {}

    uid = random.randint(1, 511)
    timestamp = int(time.time())
    privilege_expired_ts = timestamp + 3600
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(
        appId=AGORA_APP_ID,
        appCertificate=AGORA_APP_CERTIFICATE,
        channelName=channel,
        uid=uid,
        role=role,
        privilegeExpiredTs=privilege_expired_ts,
    )

    context["token"] = token
    context["uid"] = uid
    context["name"] = request.user.name
    context["channel"] = channel
    context["is_direct_request"] = True

    return render(request, "conference/room.html", context)


def get_token_view(request, *args, **kwargs):
    channel_name = request.GET.get("channel")
    uid = random.randint(1, 511)
    timestamp = int(time.time())
    privilege_expired_ts = timestamp + 3600
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(
        appId=AGORA_APP_ID,
        appCertificate=AGORA_APP_CERTIFICATE,
        channelName=channel_name,
        uid=uid,
        role=role,
        privilegeExpiredTs=privilege_expired_ts,
    )
    return JsonResponse({"token": token, "uid": uid}, safe=False)


@csrf_exempt
def create_member_view(request, *args, **kwargs):
    user = request.user
    data = json.loads(request.body)

    member, created = RoomMember.objects.get_or_create(
        user=user,
        uid=data["uid"],
        room_name=data["room_name"],
    )
    return JsonResponse({"created": created, "name": member.user.name}, safe=False)


def get_member_view(request, *args, **keargs):
    uid = request.GET.get("uid")
    room_name = request.GET.get("room_name")

    member = RoomMember.objects.get(uid=uid, room_name=room_name)
    name = member.user.name
    return JsonResponse({"name": name}, safe=False)


@csrf_exempt
def delete_member_view(request, *args, **kwargs):
    user = request.user
    data = json.loads(request.body)

    member = RoomMember.objects.get(
        user=user,
        uid=data["uid"],
        room_name=data["room_name"],
    )
    member.delete()
    return JsonResponse("member deleted", safe=False)
