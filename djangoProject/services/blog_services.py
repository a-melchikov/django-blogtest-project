from django.db.models import Q
from django.contrib.auth.models import User
from blog.models import Post, Comment
from subscriptions.models import Subscription
from notifications.models import Notification


def get_filtered_posts(user):
    queryset = Post.objects.all()
    if user.is_authenticated:
        subscribed_authors = user.subscriptions.values_list("author__id", flat=True)
        queryset = queryset.filter(
            Q(for_subscribers=False)
            | Q(author__id__in=subscribed_authors)
            | Q(author=user)
        ).order_by("-publish_date")
    else:
        queryset = queryset.filter(for_subscribers=False).order_by("-publish_date")
    return queryset


def get_author_subscribers(posts, user):
    authors = {post.author_id: post.author for post in posts}
    author_subscribers = {
        author_id: list(
            User.objects.filter(subscriptions__subscriber=user, id=author_id)
        )
        for author_id in authors.keys()
    }
    return author_subscribers


def handle_comment_form(post, user, form):
    comment = form.save(commit=False)
    comment.post = post
    comment.author = user
    comment.save()
    categories = form.cleaned_data.get("categories")
    if categories:
        post.categories.add(*categories)

    sender_name = user.username
    comments = Comment.objects.filter(post=post)
    for com in comments:
        if not Notification.objects.filter(
            Q(user=com.post.author) & Q(message=f"Новый комментарий: {com.text}")
        ).exists():
            Notification.objects.create(
                user=com.post.author,
                sender_name=sender_name,
                message=f"Новый комментарий: {com.text}",
                is_new=True,
            )
    return comment


def get_user_posts(user):
    return Post.objects.filter(author=user).order_by("-publish_date")


def create_new_post(form, user):
    post = form.save(commit=False)
    post.author = user
    post.for_subscribers = form.cleaned_data.get("for_subscribers", False)
    post.save()
    form.save_m2m()
    subscribers = Subscription.objects.filter(author=user)
    for subscriber in subscribers:
        Notification.objects.create(
            user=subscriber.subscriber,
            sender=user,
            sender_name=user.username,
            message=f"Новый пост: <a href='{post.get_absolute_url()}'>{post.title}</a>",
            is_new=True,
        )
    return post
