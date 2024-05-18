from typing import List, Union
from django.contrib.auth.models import User
from notifications.models import Notification
from messaging.models import Message


def get_messages_for_user(
    user: User, filter_name: Union[str, None] = None
) -> List[Message]:
    """
    Получает сообщения для конкретного пользователя, при необходимости фильтруя их по имени отправителя.

    args:
        user (User): Пользователь, для которого нужно получить сообщения.
        filter_name (str, optional): Имя отправителя для фильтрации сообщений. По умолчанию None.

    return:
        List[Message]: Список сообщений.
    """
    messages = Message.objects.filter(recipient=user).order_by("-timestamp")
    if filter_name:
        messages = messages.filter(sender__username=filter_name)
    return list(messages)


def send_message_from_user_to_user(
    sender: User, recipient_username: str, subject: str, body: str
) -> None:
    """
    Отправляет сообщение от одного пользователя другому.

    args:
        sender (User): Пользователь, отправляющий сообщение.
        recipient_username (str): Имя пользователя-получателя.
        subject (str): Тема сообщения.
        body (str): Текст сообщения.

    return:
        None
    """
    recipient = User.objects.get(username=recipient_username)
    message = Message(sender=sender, recipient=recipient, subject=subject, body=body)
    message.save()

    sender_name = sender.username
    Notification.objects.create(
        user=recipient,
        sender=sender,
        sender_name=sender_name,
        message=f"Новое сообщение: {message.subject}",
        is_new=True,
    )


def get_user_suggestions_by_text(input_text: str) -> List[str]:
    """
    Получает предложения имен пользователей на основе введенного текста.

    args:
        input_text (str): Входной текст для сопоставления с именами пользователей.

    return:
        List[str]: Список предлагаемых имен пользователей.
    """
    users = User.objects.filter(username__icontains=input_text)[:5]
    suggestions = [user.username for user in users]
    return suggestions


def get_sent_messages_for_user(user: User) -> List[Message]:
    """
    Получает отправленные сообщения для конкретного пользователя.

    args:
        user (User): Пользователь, для которого нужно получить отправленные сообщения.

    return:
        List[Message]: Список отправленных сообщений.
    """
    return list(Message.objects.filter(sender=user).order_by("-timestamp"))
