import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from authentication.models import Profile
from subscriptions.models import Subscription
from notifications.models import Notification
from blog.models import Post
from services.subscription_services import (
    subscribe_user_to_author,
    unsubscribe_user_from_author,
    get_post_by_id,
    get_user_by_id,
    get_user_by_username,
    get_subscriber_profiles,
)


class SubscriptionServicesTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        self.profile1 = Profile.objects.create(user=self.user1)
        self.profile2 = Profile.objects.create(user=self.user2)

        self.post = Post.objects.create(
            author=self.user1, title="Test Post", body="Test Content"
        )

    def test_subscribe_user_to_author(self):
        response = subscribe_user_to_author(self.user1, self.user2.id)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Subscription.objects.filter(
                subscriber=self.user1, author=self.user2
            ).exists()
        )
        self.assertTrue(
            Notification.objects.filter(user=self.user2, sender=self.user1).exists()
        )

    def test_unsubscribe_user_from_author(self):
        Subscription.objects.create(subscriber=self.user1, author=self.user2)
        response = unsubscribe_user_from_author(self.user1, self.user2.id)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Subscription.objects.filter(
                subscriber=self.user1, author=self.user2
            ).exists()
        )

    def test_get_post_by_id(self):
        post = get_post_by_id(self.post.id)
        self.assertEqual(post, self.post)

    def test_get_user_by_id(self):
        user = get_user_by_id(self.user1.id)
        self.assertEqual(user, self.user1)

    def test_get_user_by_username(self):
        user = get_user_by_username(self.user1.username)
        self.assertEqual(user, self.user1)

    def test_get_subscriber_profiles(self):
        Subscription.objects.create(subscriber=self.user1, author=self.user2)
        subscribers = get_subscriber_profiles(self.user2)
        self.assertEqual(len(subscribers), 1)
        self.assertEqual(subscribers[0], self.profile1)


if __name__ == "__main__":
    unittest.main()
