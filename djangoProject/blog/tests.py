from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Message, Comment, Notification


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.post = Post.objects.create(
            title="Test Post", author=self.user, body="This is a test post"
        )
        self.message = Message.objects.create(
            sender=self.user,
            recipient=self.user,
            subject="Test Subject",
            body="This is a test message",
        )
        self.comment = Comment.objects.create(
            post=self.post, author=self.user, text="This is a test comment"
        )
        self.notification = Notification.objects.create(
            user=self.user, message="Test Notification"
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.body, "This is a test post")

    def test_message_creation(self):
        self.assertEqual(self.message.sender, self.user)
        self.assertEqual(self.message.recipient, self.user)
        self.assertEqual(self.message.subject, "Test Subject")
        self.assertEqual(self.message.body, "This is a test message")

    def test_comment_creation(self):
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.text, "This is a test comment")

    def test_notification_creation(self):
        self.assertEqual(self.notification.user, self.user)
        self.assertEqual(self.notification.message, "Test Notification")

    def test_comment_approval(self):
        self.assertTrue(self.comment.approved_comment)
        self.comment.approve()
        self.assertTrue(self.comment.approved_comment)


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.post = Post.objects.create(
            title="Test Post", author=self.user, body="This is a test post"
        )
        self.comment = Comment.objects.create(
            post=self.post, author=self.user, text="This is a test comment"
        )

    def test_blog_list_view(self):
        response = self.client.get(reverse("blog_list"))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, "home.html")

    def test_blog_detail_view(self):
        response = self.client.get(reverse("post_detail", args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "post_detail.html")

    def test_create_post_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            reverse("create_post"),
            {"title": "New Test Post", "body": "This is a new test post"},
        )
        self.assertEqual(response.status_code, 302)

    def test_my_posts_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("my_posts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "my_posts.html")

    def test_edit_post_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            reverse("edit_post", args=[self.post.pk]),
            {"title": "Updated Test Post", "body": "This is an updated test post"},
        )
        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(reverse("delete_post", args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)

    def test_inbox_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("inbox"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inbox.html")

    def test_send_message_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("send_message"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "send_message.html")

    def test_user_profile_view(self):
        response = self.client.get(reverse("user_profile", args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")

    def test_all_profiles_view(self):
        response = self.client.get(reverse("all_profiles"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "all_profiles.html")

    def test_notifications_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("notifications"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notifications.html")
