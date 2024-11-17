from django.contrib import admin
from .models import UserSession

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'username', 'first_name', 'created_at']
    search_fields = ['telegram_id', 'username', 'first_name']
    readonly_fields = ['created_at']