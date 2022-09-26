from django.contrib import admin
from django_message.models import MessageThread

from .models import ChatRoom, Post


class CommonAdmin(admin.ModelAdmin):
    fields = (
        'title',
        'message_thread',
    )
    list_display = (
        'id',
        'title',
        'message_count',
        'not_readed_count',
    )

    def get_readonly_fields(self, request, obj=None):
        if not obj or (obj and obj.message_thread):
            return ('message_thread', )
        else:
            return []

    def message_count(self, obj):
        return obj.message_count

    def not_readed_count(self, obj):
        return obj.not_readed_count

    def get_queryset(self, request):
        return self.model.objects.get_queryset(request.user.id)

    def save_model(self, request, obj, form, change):
        if not obj.message_thread:
            obj.message_thread = MessageThread.objects.create()
        obj.save()


admin.site.register(ChatRoom, CommonAdmin)
admin.site.register(Post, CommonAdmin)
