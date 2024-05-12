from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "sender", "recipient", "timestamp", "read")
    list_filter = ("sender", "recipient", "timestamp", "read")
    search_fields = ("subject", "body")
    ordering = ("-timestamp",)
