from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "timestamp", "is_new", "viewed")
    list_filter = ("timestamp", "is_new", "viewed", "user")
    search_fields = ("message",)
    ordering = ("-timestamp",)
