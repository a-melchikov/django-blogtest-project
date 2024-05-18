# services/subscription_services.py
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from notifications.models import Notification
from blog.models import Post
from subscriptions.models import Subscription


def subscribe_user_to_author(subscriber: User, author_id: int) -> HttpResponseRedirect:
    """
    Подписывает пользователя на автора и создает уведомление для автора.

    args:
        subscriber (User): Пользователь, который подписывается.
        author_id (int): ID автора, на которого подписываются.

    return:
        HttpResponseRedirect: Перенаправление на профиль автора.
    """
    author = get_object_or_404(User, id=author_id)
    if subscriber != author:
        Subscription.objects.get_or_create(subscriber=subscriber, author=author)
        Notification.objects.create(
            user=author,
            sender=subscriber,
            sender_name=subscriber.username,
            message=f"Пользователь {subscriber.username} подписался на ваши обновления: -",
            is_new=True,
        )
    return HttpResponseRedirect(reverse("user_profile", args=[author.username]))


def unsubscribe_user_from_author(
    subscriber: User, author_id: int
) -> HttpResponseRedirect:
    """
    Отписывает пользователя от автора.

    args:
        subscriber (User): Пользователь, который отписывается.
        author_id (int): ID автора, от которого отписываются.

    return:
        HttpResponseRedirect: Перенаправление на профиль автора.
    """
    author = get_object_or_404(User, id=author_id)
    Subscription.objects.filter(subscriber=subscriber, author=author).delete()
    return HttpResponseRedirect(reverse("user_profile", args=[author.username]))


def get_post_by_id(post_id: int) -> Post:
    """
    Получает пост по ID.

    args:
        post_id (int): ID поста.

    return:
        Post: Экземпляр поста.
    """
    return get_object_or_404(Post, pk=post_id)


def get_user_by_id(user_id: int) -> User:
    """
    Получает пользователя по ID.

    args:
        user_id (int): ID пользователя.

    return:
        User: Экземпляр пользователя.
    """
    return get_object_or_404(User, id=user_id)


def get_user_by_username(username: str) -> User:
    """
    Получает пользователя по имени пользователя.

    args:
        username (str): Имя пользователя.

    return:
        User: Экземпляр пользователя.
    """
    return get_object_or_404(User, username=username)


def get_subscriber_profiles(author: User):
    """
    Получает профили подписчиков автора.

    args:
        author (User): Автор, чьи подписчики нужны.

    return:
        list: Список профилей подписчиков.
    """
    subscriptions = Subscription.objects.filter(author=author)
    return [subscription.subscriber.profile for subscription in subscriptions]
