from django.urls import path
from .views import (
    delete_all_notifications,
    delete_notification,
    mark_all_as_viewed,
    mark_as_viewed,
    notifications,
)

urlpatterns = [
    path("notifications/", notifications, name="notifications"),
    path(
        "delete_all_notifications/",
        delete_all_notifications,
        name="delete_all_notifications",
    ),
    path(
        "mark_as_viewed/<int:notification_id>/", mark_as_viewed, name="mark_as_viewed"
    ),
    path("mark_all_as_viewed/", mark_all_as_viewed, name="mark_all_as_viewed"),
    path(
        "delete_notification/<int:notification_id>/",
        delete_notification,
        name="delete_notification",
    ),
]
