import random
import string

from django.shortcuts import render, redirect
from .models import *


def generate_random_string(length=14):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def create_room(request):
    if request.method == 'POST':
        username = request.user.nickname # 나
        # room = request.POST['room'] # 채팅방 이름(나 + 상대닉네임 사전순으로 배열 + 합쳐서 해싱)
        room = 'uaBSvqKvdVYQsa'

        try:
            get_room = Room.objects.get(room_name=room)
            return redirect('room', room_name=room, username=username)

        except Room.DoesNotExist:
            new_room = Room(room_name=room)
            new_room.save()
            return redirect('room', room_name=room, username=username)
    return render(request, 'chat/room.html', context={'user': request.user})


def message_view(request, room_name, username):
    get_room = Room.objects.get(room_name=room_name)

    if request.method == 'POST':
        message = request.POST['message']

        new_message = Message(room=get_room, sender=username, message=message)
        new_message.save()

    get_messages = Message.objects.filter(room=get_room)

    context = {
        "messages": get_messages,
        "username": username,
        "user": request.user,
        "room_name": room_name,
    }
    return render(request, 'chat/room.html', context)