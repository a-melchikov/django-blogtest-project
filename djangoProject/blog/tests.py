from django.http import Http404
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Post, Category, Comment, Favorite
from services.paginators import GeneralPaginator
from subscriptions.models import Subscription
from services.blog_services import (
    toggle_post_like,
    get_subscribed_posts,
    toggle_favorite_post,
    get_favorite_posts,
    get_blog_queryset,
    get_blog_context,
    get_post_comments,
    is_favorite_post,
    create_post_for_user,
    get_user_posts,
    get_all_categories,
    get_post_by_id,
    check_user_permission_to_edit_post,
    handle_edit_post_form,
    get_post_edit_context,
    get_category_by_slug,
    get_posts_by_category,
    get_posts_by_query,
    get_paginated_posts,
)


class ServiceTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user(username="user1", password="pass")
        self.user2 = User.objects.create_user(username="user2", password="pass")

        self.category1 = Category.objects.create(name="Category1", slug="category1")
        self.category2 = Category.objects.create(name="Category2", slug="category2")

        self.post1 = Post.objects.create(
            title="Post 1",
            body="Body of post 1",
            author=self.user1,
            for_subscribers=True,
        )
        self.post2 = Post.objects.create(
            title="Post 2",
            body="Body of post 2",
            author=self.user2,
            for_subscribers=False,
        )

        self.comment1 = Comment.objects.create(
            post=self.post1, author=self.user2, text="Comment 1", approved_comment=True
        )

        self.subscription1 = Subscription.objects.create(
            subscriber=self.user1, author=self.user2
        )

        self.favorite1 = Favorite.objects.create(user=self.user1, post=self.post2)

    def test_toggle_post_like(self):
        toggle_post_like(self.post1.id, self.user1)
        self.assertIn(self.user1, self.post1.likes.all())
        toggle_post_like(self.post1.id, self.user1)
        self.assertNotIn(self.user1, self.post1.likes.all())

    def test_get_subscribed_posts(self):
        context = get_subscribed_posts(self.user1)
        self.assertIn(self.post2, context["page_obj"].object_list)

    def test_toggle_favorite_post(self):
        toggle_favorite_post(self.post1.id, self.user1)
        self.assertTrue(is_favorite_post(self.user1, self.post1))
        toggle_favorite_post(self.post1.id, self.user1)
        self.assertFalse(is_favorite_post(self.user1, self.post1))

    def test_get_favorite_posts(self):
        context = get_favorite_posts(self.user1)
        self.assertIn(self.favorite1, context["page_obj"].object_list)

    def test_get_blog_queryset(self):
        queryset = get_blog_queryset(self.user1, "-publish_date")
        self.assertIn(self.post1, queryset)
        self.assertIn(self.post2, queryset)

    def test_get_blog_context(self):
        paginator = GeneralPaginator(Post.objects.all())
        context = get_blog_context(self.user1, Post.objects.all(), paginator, 1)
        self.assertIn("posts", context)

    def test_get_post_comments(self):
        comments = get_post_comments(self.post1)
        self.assertIn(self.comment1, comments)

    def test_is_favorite_post(self):
        self.assertTrue(is_favorite_post(self.user1, self.post2))

    def test_create_post_for_user(self):
        request = self.factory.post(
            reverse("create_post"),
            {"title": "New Post", "body": "New Content", "for_subscribers": "on"},
        )
        request.user = self.user1
        form = create_post_for_user(request)
        self.assertTrue(form.is_valid())

    def test_get_user_posts(self):
        posts = get_user_posts(self.user1)
        self.assertIn(self.post1, posts)

    def test_get_all_categories(self):
        categories = get_all_categories()
        self.assertIn(self.category1, categories)
        self.assertIn(self.category2, categories)

    def test_get_post_by_id(self):
        post = get_post_by_id(self.post1.id)
        self.assertEqual(post, self.post1)

    def test_check_user_permission_to_edit_post(self):
        with self.assertRaises(Http404):
            check_user_permission_to_edit_post(self.user2, self.post1)

    def test_handle_edit_post_form(self):
        request = self.factory.post(
            reverse("edit_post", args=[self.post1.pk]),
            {"title": "Updated Post", "body": "Updated Content"},
        )
        request.user = self.user1
        form = handle_edit_post_form(request, self.post1)
        self.assertTrue(form.is_valid())

    def test_get_post_edit_context(self):
        context = get_post_edit_context(self.post1)
        self.assertIn("categories", context)
        self.assertIn("selected_categories", context)

    def test_get_category_by_slug(self):
        category = get_category_by_slug(self.category1.slug)
        self.assertEqual(category, self.category1)

    # def test_get_posts_by_category_authenticated(self):
    #     posts = get_posts_by_category(self.category1, self.user1)
    #     self.assertIn(self.post1, posts)
    #     self.assertIn(self.post2, posts)

    def test_get_posts_by_query(self):
        posts = get_posts_by_query("Post 1", self.user1)
        self.assertIn(self.post1, posts)

    def test_get_paginated_posts(self):
        request = self.factory.get(reverse("blog_list"))
        context = get_paginated_posts(
            request, Post.objects.all().order_by("-publish_date")
        )
        self.assertIn("page_obj", context)
