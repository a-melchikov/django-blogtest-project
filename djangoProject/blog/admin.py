from django import forms
from django.contrib import admin
from .models import Category, Like, Notification, Post, Message, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publish_date")
    list_filter = ("author", "publish_date", "categories")
    search_fields = ("title", "body")
    ordering = ("-publish_date",)
    filter_horizontal = ("categories",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "sender", "recipient", "timestamp", "read")
    list_filter = ("sender", "recipient", "timestamp", "read")
    search_fields = ("subject", "body")
    ordering = ("-timestamp",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "text", "created_date", "approved_comment")
    list_filter = ("post", "author", "created_date", "approved_comment")
    search_fields = ("text",)
    ordering = ("-created_date",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "timestamp", "is_new", "viewed")
    list_filter = ("timestamp", "is_new", "viewed", "user")
    search_fields = ("message",)
    ordering = ("-timestamp",)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "like")
    list_filter = ("like",)
    search_fields = ("user__username", "post__title")


admin.site.site_header = "Управление блогом"
admin.site.site_title = "Администрирование"
admin.site.index_title = "Главная страница административной панели"
