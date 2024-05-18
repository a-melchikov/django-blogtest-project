from typing import List
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from notifications.models import Notification


def get_notifications_for_user(user: User) -> List[Notification]:
    """
    Получает все новые уведомления для пользователя и помечает их тип и текст.

    args:
        user (User): Пользователь, для которого нужно получить уведомления.

    return:
        List[Notification]: Список уведомлений.
    """
    notifications = Notification.objects.filter(user=user, is_new=True).order_by("-id")
    for notification in notifications:
        notification.type, notification.text = str(notification).split(":")
    return notifications


def get_not_viewed_count_for_user(user: User) -> int:
    """
    Получает количество непросмотренных уведомлений для пользователя.

    args:
        user (User): Пользователь, для которого нужно получить количество непросмотренных уведомлений.

    return:
        int: Количество непросмотренных уведомлений.
    """
    return Notification.objects.filter(user=user, viewed=False).count()


def delete_notification_for_user(user: User, notification_id: int) -> bool:
    """
    Удаляет уведомление для пользователя.

    args:
        user (User): Пользователь, удаляющий уведомление.
        notification_id (int): Идентификатор удаляемого уведомления.

    return:
        bool: True, если уведомление было удалено, иначе False.
    """
    notification = get_object_or_404(Notification, id=notification_id)
    if user == notification.user:
        notification.delete()
        return True
    return False


def delete_all_notifications_for_user(user: User) -> None:
    """
    Удаляет все уведомления для пользователя.

    args:
        user (User): Пользователь, для которого нужно удалить все уведомления.

    return:
        None
    """
    Notification.objects.filter(user=user).delete()


def mark_notification_as_viewed(user: User, notification_id: int) -> bool:
    """
    Отмечает уведомление как просмотренное для пользователя.

    args:
        user (User): Пользователь, отмечающий уведомление.
        notification_id (int): Идентификатор уведомления, которое нужно отметить.

    return:
        bool: True, если уведомление было отмечено, иначе False.
    """
    notification = get_object_or_404(Notification, id=notification_id)
    if user == notification.user:
        notification.viewed = True
        notification.save()
        return True
    return False


def mark_all_notifications_as_viewed(user: User) -> None:
    """
    Отмечает все уведомления как просмотренные для пользователя.

    args:
        user (User): Пользователь, для которого нужно отметить все уведомления.

    return:
        None
    """
    Notification.objects.filter(user=user, viewed=False).update(viewed=True)
