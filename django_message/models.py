from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

AUTH_USER_MODEL = get_user_model()


class MessageThread(models.Model):
    pass


class Participant(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    readed_at = models.DateTimeField(auto_now=True)
    thread = models.ForeignKey(
        MessageThread,
        models.CASCADE,
        related_name='participants',
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        models.SET_NULL,
        related_name='message_thread_participants',
        null=True,
    )

    def __str__(self):
        return ''


class Message(models.Model):
    participant = models.ForeignKey(
        Participant,
        models.CASCADE,
        related_name='messages',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return '%s, %s' % (self.participant.user, self.created_at)

    @property
    def change_url(self):
        return reverse('admin:django_message_message_change', args=[self.id])

    class Meta:
        ordering = ['created_at']
