from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe

if 'nested_admin' in settings.INSTALLED_APPS:
    from nested_admin import nested

from django_message.models import Message, MessageThread, Participant

if 'nested_admin' in settings.INSTALLED_APPS:
    class MessageInline(nested.NestedTabularInline):
        verbose_name_plural = 'send'
        model = Message
        max_num = 1

        def get_queryset(self, request):
            return self.model.objects.none()


    class ParticipantInline(nested.NestedTabularInline):
        class form(forms.ModelForm):
            class Meta:
                model = Participant
                fields = []

            def save(self, commit=True):
                self.instance.user = self.request.user
                return super().save(commit)
        
        verbose_name_plural = ''
        model = Participant
        max_num = 1
        inlines = (
            MessageInline,
        )

        def has_delete_permission(self, request, obj=None):
            return False

        def get_queryset(self, request):
            return self.model.objects.filter(user_id=request.user.id)


    @admin.register(MessageThread)
    class MessageThreadAdmin(nested.NestedModelAdmin):
        fields = (
            'messages',
        )
        readonly_fields = (
            'messages',
        )
        list_display = ('id', )
        inlines = (
            ParticipantInline,
        )

        def build_message_change_url(self, msg):
            f = ' <a href="%s">edit</a>'
            if self.request.user == msg.participant.user:
                return f % msg.change_url
            else:
                return ''

        def messages(self, obj):
            return mark_safe('<br/><br/>'.join([
                str(m) + self.build_message_change_url(m) + '<br/>%s' % m.content
                for m in Message.objects.filter(participant__thread_id=obj.id)
            ]))

        def get_queryset(self, request):
            self.request = request
            return super().get_queryset(request)

        def save_formset(self, request, form, formset, change):
            for form in formset.forms:
                form.request = request
            formset.save()


    @admin.register(Message)
    class MessageAdmin(admin.ModelAdmin):
        list_display = (
            'created_at',
            'content',
        )
        fields = (
            'content',
        )

        def has_add_permission(self, request):
            return False

        def has_change_permission(self, request, obj=None):
            return (
                super().has_change_permission(request, obj) and
                obj and obj.participant.user == request.user
            )

