from django.contrib import admin
from .models import Category, Favorite, Like, Notification, Post, Comment, Subscription


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publish_date")
    list_filter = ("author", "publish_date", "categories")
    search_fields = ("title", "body")
    ordering = ("-publish_date",)
    filter_horizontal = ("categories",)


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


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("subscriber", "author")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "post")
    search_fields = ("user__username", "post__title")


admin.site.site_header = "Управление блогом"
admin.site.site_title = "Администрирование"
admin.site.index_title = "Главная страница административной панели"
