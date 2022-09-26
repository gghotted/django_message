from django.db import models
from django_message.managers import ClientManager


class ChatRoom(models.Model):
    title = models.CharField(max_length=100)
    message_thread = models.OneToOneField(
        'django_message.MessageThread',
        models.SET_NULL,
        null=True,
    )
    
    objects = ClientManager()


class Post(models.Model):
    title = models.CharField(max_length=100)
    message_thread = models.OneToOneField(
        'django_message.MessageThread',
        models.SET_NULL,
        null=True,
    )

    objects = ClientManager()
