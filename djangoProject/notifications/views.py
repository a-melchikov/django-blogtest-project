from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from services.notifications_services import (
    get_notifications_for_user,
    get_not_viewed_count_for_user,
    delete_notification_for_user,
    delete_all_notifications_for_user,
    mark_notification_as_viewed,
    mark_all_notifications_as_viewed,
)


@login_required
def notifications(request):
    user_notifications = get_notifications_for_user(request.user)
    not_viewed_count = get_not_viewed_count_for_user(request.user)

    return render(
        request,
        "notification/notifications.html",
        {"notifications": user_notifications, "notifications_count": not_viewed_count},
    )


@login_required
def delete_notification(request, notification_id):
    if delete_notification_for_user(request.user, notification_id):
        return redirect("notifications")
    return HttpResponseForbidden("Вы не имеете прав на удаление этого уведомления.")


@login_required
def delete_all_notifications(request):
    if request.method == "POST":
        delete_all_notifications_for_user(request.user)
        return redirect("notifications")


@login_required
def mark_as_viewed(request, notification_id):
    if mark_notification_as_viewed(request.user, notification_id):
        return redirect("notifications")
    return HttpResponseForbidden(
        "Вы не имеете прав на отметку этого уведомления как просмотренного."
    )


@login_required
def mark_all_as_viewed(request):
    mark_all_notifications_as_viewed(request.user)
    return redirect("notifications")
