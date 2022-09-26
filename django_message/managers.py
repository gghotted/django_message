from django.db import models
from django.db.models import Count, F, Q


class MessageCount(Count):
    def __init__(self):
        super().__init__('message_thread__participants__messages')


class MessageNotReadedCount(Count):
    def __init__(self, user_id=None):
        super().__init__(
            'message_thread__participants__messages',
            filter=(
                Q(message_thread__participants__messages__created_at__gte=F('message_thread__participants__readed_at')) &
                Q(message_thread__participants__user_id=user_id)
            )
        )


class ClientManager(models.Manager):
    def get_queryset(self, user_id=None):
        return super().get_queryset() \
                      .annotate(message_count=MessageCount()) \
                      .annotate(not_readed_count=MessageNotReadedCount(user_id))
