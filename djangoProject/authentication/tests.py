from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User

from blog.models import Post
from authentication.models import Profile
from authentication.forms import ProfileForm, UserForm
from services.authentication_services import (
    authenticate_user,
    login_user,
    logout_user,
    create_user,
    get_user_by_username,
    get_user_posts,
    get_user_subscriptions,
    check_user_subscription,
    filter_user_posts,
)


class AuthenticationServicesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.profile = Profile.objects.create(user=self.user)
        self.factory = RequestFactory()
        self.request = self.factory.get("/")
        self.request.user = self.user
        self.request.session = self.client.session

    def test_authenticate_user(self):
        user = authenticate_user(self.request, "testuser", "password")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")

    def test_login_user(self):
        login_user(self.request, self.user)
        self.assertTrue(self.request.user.is_authenticated)

    def test_logout_user(self):
        self.client.login(username="testuser", password="password")
        self.request.user = self.user
        logout_user(self.request)
        self.assertFalse("_auth_user_id" in self.request.session)

    def test_create_user(self):
        user_form_data = {
            "username": "newuser",
            "password1": "password",
            "password2": "password",
        }
        profile_form_data = {"bio": "New user bio"}
        user_form = UserForm(data=user_form_data)
        profile_form = ProfileForm(data=profile_form_data)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = create_user(user_form, profile_form)
            self.assertEqual(new_user.username, "newuser")
            self.assertTrue(Profile.objects.filter(user=new_user).exists())

    def test_get_user_by_username(self):
        user = get_user_by_username("testuser")
        self.assertEqual(user.username, "testuser")

    def test_get_user_posts(self):
        post = Post.objects.create(
            author=self.user, title="Test Post", body="Test content"
        )
        user_posts = get_user_posts(self.user)
        self.assertIn(post, user_posts)

    def test_get_user_subscriptions(self):
        subscriptions = get_user_subscriptions(self.user)
        self.assertEqual(len(subscriptions), 0)

    def test_check_user_subscription(self):
        target_user = User.objects.create_user(
            username="targetuser", password="password"
        )
        is_subscribed = check_user_subscription(self.user, target_user)
        self.assertFalse(is_subscribed)

    def test_filter_user_posts(self):
        post1 = Post.objects.create(author=self.user, title="Post 1", body="Content 1")
        post2 = Post.objects.create(
            author=self.user, title="Post 2", body="Content 2", for_subscribers=True
        )
        post3 = Post.objects.create(author=self.user, title="Post 3", body="Content 3")

        user_posts = get_user_posts(self.user)
        filtered_posts = filter_user_posts(user_posts, self.user, [])

        self.assertIn(post1, filtered_posts)
        self.assertIn(post2, filtered_posts)
        self.assertIn(post3, filtered_posts)

        other_user = User.objects.create_user(username="otheruser", password="password")
        other_post = Post.objects.create(
            author=other_user,
            title="Other Post",
            body="Other content",
            for_subscribers=True,
        )

        other_user_posts = get_user_posts(other_user)
        filtered_other_user_posts = filter_user_posts(other_user_posts, self.user, [])

        self.assertNotIn(other_post, filtered_other_user_posts)
