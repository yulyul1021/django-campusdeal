from django.db import models
from django.utils import timezone
from user.models import User


class Room(models.Model):
    room_name = models.CharField(max_length=255)    # pk만 있어도 될듯?

    def __str__(self):
        return self.room_name

    def return_room_messages(self):
        return Message.objects.filter(room=self)

    def create_new_room_message(self, sender, message):
        new_message = Message(room=self, sender=sender, message=message)
        new_message.save()


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)   # 보낸사람 / 유저로 변경해야함
    message = models.TextField()
    # sent_date = models.DateTimeField(default=timezone.now())  # + 언제 보내졌는지

    def __str__(self):
        return str(self.room)