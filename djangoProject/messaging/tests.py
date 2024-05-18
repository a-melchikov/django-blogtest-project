import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from notifications.models import Notification
from messaging.models import Message
from services.messaging_services import (
    get_messages_for_user,
    send_message_from_user_to_user,
    get_user_suggestions_by_text,
    get_sent_messages_for_user,
)


class MessagingServicesTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")

    def test_get_messages_for_user(self):
        Message.objects.create(
            sender=self.user2,
            recipient=self.user1,
            subject="Test Subject 1",
            body="Test Body 1",
        )
        Message.objects.create(
            sender=self.user2,
            recipient=self.user1,
            subject="Test Subject 2",
            body="Test Body 2",
        )

        messages = get_messages_for_user(self.user1)
        self.assertEqual(len(messages), 2)

        messages = get_messages_for_user(self.user1, filter_name="user2")
        self.assertEqual(len(messages), 2)

        messages = get_messages_for_user(self.user1, filter_name="nonexistent")
        self.assertEqual(len(messages), 0)

    def test_send_message_from_user_to_user(self):
        send_message_from_user_to_user(self.user1, "user2", "Test Subject", "Test Body")

        messages = Message.objects.filter(sender=self.user1, recipient=self.user2)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].subject, "Test Subject")
        self.assertEqual(messages[0].body, "Test Body")

        notifications = Notification.objects.filter(user=self.user2, sender=self.user1)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0].message, "Новое сообщение: Test Subject")

    def test_get_user_suggestions_by_text(self):
        User.objects.create_user(username="user3", password="password3")
        User.objects.create_user(username="anotheruser", password="password4")

        suggestions = get_user_suggestions_by_text("user")
        self.assertIn("user1", suggestions)
        self.assertIn("user2", suggestions)
        self.assertIn("user3", suggestions)
        self.assertIn("anotheruser", suggestions)
        self.assertNotIn("petya", suggestions)

        suggestions = get_user_suggestions_by_text("nonexistent")
        self.assertEqual(len(suggestions), 0)

    def test_get_sent_messages_for_user(self):
        Message.objects.create(
            sender=self.user1,
            recipient=self.user2,
            subject="Test Subject 1",
            body="Test Body 1",
        )
        Message.objects.create(
            sender=self.user1,
            recipient=self.user2,
            subject="Test Subject 2",
            body="Test Body 2",
        )

        messages = get_sent_messages_for_user(self.user1)
        self.assertEqual(len(messages), 2)

        self.assertEqual(messages[0].subject, "Test Subject 2")
        self.assertEqual(messages[1].subject, "Test Subject 1")


if __name__ == "__main__":
    unittest.main()
