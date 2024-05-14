from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect

from .models import Notification


@login_required
def notifications(request):
    user = request.user
    not_viewed_count = Notification.objects.filter(user=user, viewed=False).count()
    user_notifications = Notification.objects.filter(user=user, is_new=True)[::-1]

    for notification in user_notifications:
        notification.type, notification.text = str(notification).split(":")

    return render(
        request,
        "notification/notifications.html",
        {"notifications": user_notifications, "notifications_count": not_viewed_count},
    )


@login_required
def delete_all_notifications(request):
    if request.method == "POST":
        Notification.objects.filter(user=request.user).delete()
        return redirect("notifications")


@login_required
def mark_as_viewed(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    if request.user == notification.user:
        notification.viewed = True
        notification.save()
        return redirect("notifications")
    else:
        return HttpResponseForbidden(
            "Вы не имеете прав на отметку этого уведомления как просмотренного."
        )


@login_required
def mark_all_as_viewed(request):
    user_notifications = Notification.objects.filter(user=request.user, viewed=False)
    user_notifications.update(viewed=True)
    return redirect("notifications")
