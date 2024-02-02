from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ChatSession, Message


class MessageInline(admin.TabularInline):  # You can also use admin.StackedInline for a different layout
    model = Message
    extra = 0  # Specifies the number of blank forms to display at the end of the inline. Setting this to 0 improves page load times when you have a lot of existing related objects.
    fields = ('text', 'role', 'created_at', 'estimated_tokens', 'prompt_tokens',
              'total_tokens')  # Customize as needed. Add 'usage' to view token usage data
    readonly_fields = (
        'created_at', 'text', 'role', 'estimated_tokens', 'prompt_tokens',
        'total_tokens')  # Prevent editing of certain fields directly from the inline if desired
    can_delete = True  # Allows deletion of messages directly from the chat session admin page
    show_change_link = True  # Adds a link to the individual message admin change page


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    list_filter = ('user',)
    search_fields = ('user__username',)
    inlines = [MessageInline]  # Add the inline class here


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_text', 'role', 'chat_session_id', 'created_at')  # Customized list display
    list_filter = ('chat_session', 'role')
    search_fields = ('text', 'chat_session__user__username')

    def chat_session_id(self, obj):
        return obj.chat_session.id

    chat_session_id.short_description = 'Chat Session ID'  # Optionally set a short description

    def short_text(self, obj):
        return (obj.text[:75] + '...') if len(obj.text) > 75 else obj.text

    short_text.short_description = 'Text'  # Optionally set a short description
