import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from notifications.models import Notification
from services.notifications_services import (
    get_notifications_for_user,
    get_not_viewed_count_for_user,
    delete_notification_for_user,
    delete_all_notifications_for_user,
    mark_notification_as_viewed,
    mark_all_notifications_as_viewed,
)


class NotificationServicesTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")

        self.notification1 = Notification.objects.create(
            user=self.user1,
            sender=self.user2,
            message="type1:Test Notification 1",
            viewed=False,
            is_new=True,
        )
        self.notification2 = Notification.objects.create(
            user=self.user1,
            sender=self.user2,
            message="type2:Test Notification 2",
            viewed=False,
            is_new=True,
        )
        self.notification3 = Notification.objects.create(
            user=self.user1,
            sender=self.user2,
            message="type3:Test Notification 3",
            viewed=True,
            is_new=False,
        )

    def test_get_notifications_for_user(self):
        notifications = get_notifications_for_user(self.user1)
        self.assertEqual(len(notifications), 2)
        self.assertEqual(notifications[0].type, "type2")
        self.assertEqual(notifications[0].text, "Test Notification 2")
        self.assertEqual(notifications[1].type, "type1")
        self.assertEqual(notifications[1].text, "Test Notification 1")

    def test_get_not_viewed_count_for_user(self):
        not_viewed_count = get_not_viewed_count_for_user(self.user1)
        self.assertEqual(not_viewed_count, 2)

    def test_delete_notification_for_user(self):
        result = delete_notification_for_user(self.user1, self.notification1.id)
        self.assertTrue(result)
        self.assertFalse(Notification.objects.filter(id=self.notification1.id).exists())

        result = delete_notification_for_user(self.user2, self.notification2.id)
        self.assertFalse(result)
        self.assertTrue(Notification.objects.filter(id=self.notification2.id).exists())

    def test_delete_all_notifications_for_user(self):
        delete_all_notifications_for_user(self.user1)
        self.assertEqual(Notification.objects.filter(user=self.user1).count(), 0)

    def test_mark_notification_as_viewed(self):
        result = mark_notification_as_viewed(self.user1, self.notification1.id)
        self.assertTrue(result)
        self.notification1.refresh_from_db()
        self.assertTrue(self.notification1.viewed)

        result = mark_notification_as_viewed(self.user2, self.notification2.id)
        self.assertFalse(result)
        self.notification2.refresh_from_db()
        self.assertFalse(self.notification2.viewed)

    def test_mark_all_notifications_as_viewed(self):
        mark_all_notifications_as_viewed(self.user1)
        notifications = Notification.objects.filter(user=self.user1)
        for notification in notifications:
            self.assertTrue(notification.viewed)


if __name__ == "__main__":
    unittest.main()
