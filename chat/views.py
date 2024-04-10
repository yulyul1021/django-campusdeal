from django.shortcuts import render, redirect
from .models import *


def create_room(request):
    if request.method == 'POST':
        username = request.user.username
        room = 'UN2atUrbYvZA7oe7pIgh'

        try:
            get_room = Room.objects.get(room_name=room)
            return redirect('chatapp:room', room_name=room, username=username)

        except Room.DoesNotExist:
            new_room = Room(room_name=room)
            new_room.save()
            return redirect('chatapp:room', room_name=room, username=username)
    return render(request, 'chat/home.html')


def message_view(request, room_name, username):
    get_room = Room.objects.get(room_name=room_name)

    if request.method == 'POST':
        message = request.POST['message']

        print(message)

        new_message = Message(room=get_room, sender=username, message=message)
        new_message.save()

    get_messages = Message.objects.filter(room=get_room)

    context = {
        "messages": get_messages,
        "user": username,
        "room_name": room_name,
    }
    return render(request, 'chat/room.html', context)