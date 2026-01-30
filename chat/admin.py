from django.contrib import admin
from .models import ChatSession, ChatMessage

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    readonly_fields = ('role', 'content', 'created_at')
    extra = 0
    can_delete = False

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'title')
    inlines = [ChatMessageInline]
    readonly_fields = ('user', 'title', 'created_at')

    def has_add_permission(self, request):
        return False
