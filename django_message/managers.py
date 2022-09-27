from django.db import models
from django.db.models import Count, F, OuterRef, Q, Subquery


class MessageCount(Count):
    def __init__(self):
        super().__init__('message_thread__participants__messages')


class MessageNotReadedCount(Count):
    def __init__(self, user_id=None):
        from django_message.models import Participant

        participant_readed_at = Participant.objects.filter(
            thread=OuterRef('message_thread'),
            user_id=user_id,
        ).values('readed_at')[:1]
        super().__init__(
            'message_thread__participants__messages',
            filter=(
                Q(message_thread__participants__messages__created_at__gte=participant_readed_at)
            )
        )


class ClientManager(models.Manager):
    def get_queryset(self, user_id=None):
        return super().get_queryset() \
                      .annotate(message_count=MessageCount()) \
                      .annotate(not_readed_count=MessageNotReadedCount(user_id))
