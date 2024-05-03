from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import (
    Http404,
    HttpResponseForbidden,
    HttpResponseRedirect,
)
from django.urls import reverse, reverse_lazy
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    DeleteView,
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin


from authentication.models import Profile

from authentication.forms import ProfileForm
from .models import (
    Category,
    Favorite,
    Message,
    Notification,
    Post,
    Comment,
    Subscription,
)
from .forms import PostForm, CommentForm


class BlogList(ListView):
    model = Post
    template_name = "home.html"
    context_object_name = "posts"
    paginate_by = 5
    ordering = "-publish_date"

    def get_queryset(self):
        subscribed_authors = self.request.user.subscriptions.values_list(
            "author", flat=True
        )
        return Post.objects.filter(
            Q(for_subscribers=False)
            | Q(author__in=subscribed_authors)
            | Q(author=self.request.user)
        ).order_by(self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context["posts"], self.paginate_by)
        page_number = self.request.GET.get("page")
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context["posts"] = page_obj

        authors = {post.author_id: post.author for post in page_obj.object_list}
        author_subscribers = {
            author_id: list(
                User.objects.filter(
                    subscribers__subscriber=self.request.user, id=author_id
                )
            )
            for author_id in authors.keys()
        }
        context["author_subscribers"] = author_subscribers

        return context


class BlogDetailView(UserPassesTestMixin, DetailView):
    model = Post
    template_name = "post/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["comments"] = post.comments.filter(approved_comment=True).order_by(
            "-created_date"
        )
        context["comment_form"] = CommentForm()

        user = self.request.user
        if user.is_authenticated:
            context["is_favorite"] = post.favorite_set.filter(user=user).exists()

        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            categories = request.POST.getlist("categories")
            if categories:
                post.categories.add(*categories)

            sender_name = request.user.username

            user = request.user
            comments = Comment.objects.filter(post__author=user)
            comments = Comment.objects.filter(post=post)
            for com in comments:
                if not Notification.objects.filter(
                    Q(user=com.post.author)
                    & Q(message=f"Новый комментарий: {com.text}")
                ).exists():
                    Notification.objects.create(
                        user=com.post.author,
                        sender_name=sender_name,
                        message=f"Новый комментарий: {com.text}",
                        is_new=True,
                    )
            return HttpResponseRedirect(reverse("post_detail", args=[post.pk]))
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        post = self.get_object()
        user = self.request.user
        return (post.author == user) or user.subscriptions.filter(
            author=post.author
        ).exists()

    def handle_no_permission(self):
        raise Http404("Вы не подписаны на автора этого поста")


class AboutPageView(TemplateView):
    template_name = "about.html"


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            post.for_subscribers = request.POST.get("for_subscribers", False) == "on"
            post.save()
            form.save_m2m()

            post_detail_url = reverse("post_detail", args=[post.id])
            subscribers = Subscription.objects.filter(author=request.user)
            for subscriber in subscribers:
                Notification.objects.create(
                    user=subscriber.subscriber,
                    sender=request.user,
                    sender_name=request.user.username,
                    message=f"Новый пост: <a href='{post_detail_url}'>{post.title}</a>",
                    is_new=True,
                )

            return redirect("home")
    else:
        form = PostForm()
    categories = Category.objects.all()
    return render(
        request, "post/create_post.html", {"form": form, "categories": categories}
    )


@login_required
def my_posts(request):
    user = request.user
    user_posts = Post.objects.filter(author=user).order_by("-publish_date")
    return render(request, "post/my_posts.html", {"user_posts": user_posts})


@login_required
def edit_profile(request, user_name):
    user = get_object_or_404(User, username=user_name)

    if request.user != user:
        raise Http404("Вы не имеете прав на редактирование данного профиля")

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("user_profile", user_name=request.user.username)
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, "profile/edit_profile.html", {"form": form})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        raise Http404("Вы не имеете прав на редактирование данного поста")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("my_posts")
    else:
        form = PostForm(instance=post)

    selected_categories = post.categories.all()

    categories = Category.objects.all()
    return render(
        request,
        "post/edit_post.html",
        {
            "form": form,
            "categories": categories,
            "selected_categories": selected_categories,
        },
    )


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("my_posts")
    template_name = "post/post_confirm_delete.html"


@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by("-timestamp")
    return render(request, "messages/inbox.html", {"messages": messages})


@login_required
def send_message(request):
    if request.method == "POST":
        recipient = request.POST["recipient"]
        subject = request.POST["subject"]
        body = request.POST["body"]

        sender = request.user

        message = Message(
            sender=sender,
            recipient=Profile.objects.get(user__username=recipient).user,
            subject=subject,
            body=body,
        )
        message.save()

        sender_name = sender.username
        Notification.objects.create(
            user=message.recipient,
            sender=sender,
            sender_name=sender_name,
            message=f"Новое сообщение: {message.subject}",
            is_new=True,
        )

        return redirect("inbox")
    else:
        profiles = Profile.objects.all()
        return render(request, "messages/send_message.html", {"profiles": profiles})


@login_required
def user_profile_view(request, user_name):
    user = get_object_or_404(User, username=user_name)
    user_posts = Post.objects.filter(author=user).order_by("-publish_date")
    is_subscribed = False
    if request.user.is_authenticated:
        is_subscribed = request.user.subscriptions.filter(author=user).exists()
    subscriber_count = user.subscribers.count()
    return render(
        request,
        "profile/profile.html",
        {
            "user": user,
            "user_posts": user_posts,
            "is_subscribed": is_subscribed,
            "subscriber_count": subscriber_count,
        },
    )


class AllProfilesView(ListView):
    model = Profile
    template_name = "profile/all_profiles.html"
    context_object_name = "profile_list"

    def get_queryset(self):
        return Profile.objects.all()


@login_required
def notifications(request):
    user = request.user
    not_viewed_count = Notification.objects.filter(user=user, viewed=False).count()
    notif = Notification.objects.filter(user=user, is_new=True)[::-1]

    for notification in notif:
        notification.type, notification.text = str(notification).split(":")

    return render(
        request,
        "notification/notifications.html",
        {"notifications": notif, "notifications_count": not_viewed_count},
    )


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(categories=category).order_by("-publish_date")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "post/category_posts.html", context)


def search_posts(request):
    query = request.GET.get("query")
    if query:
        posts = (
            Post.objects.filter(
                Q(title__icontains=query)
                | Q(body__icontains=query)
                | Q(author__username__icontains=query)
            )
            .distinct()
            .order_by("-publish_date")
        )
    else:
        posts = Post.objects.all().order_by("-publish_date")
    return render(request, "search_results.html", {"posts": posts})


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if request.method == "POST":
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    if request.user == notification.user:
        notification.delete()
        return redirect("notifications")
    else:
        return HttpResponseForbidden("Вы не имеете прав на удаление этого уведомления.")


@login_required
def subscribe(request, author_id):
    author = get_object_or_404(User, id=author_id)
    if request.user != author:
        if request.method == "POST":
            Subscription.objects.get_or_create(subscriber=request.user, author=author)
            Notification.objects.create(
                user=author,
                sender=request.user,
                sender_name=request.user.username,
                message=f"Пользователь {request.user.username} подписался на ваши обновления: -",
                is_new=True,
            )
            return HttpResponseRedirect(reverse("user_profile", args=[author.username]))
        else:
            return render(request, "profile/subscribe.html", {"author": author})
    else:
        return HttpResponseRedirect(reverse("user_profile", args=[author.username]))


@login_required
def unsubscribe(request, author_id):
    author = get_object_or_404(User, id=author_id)
    if request.method == "POST":
        Subscription.objects.filter(subscriber=request.user, author=author).delete()
        return HttpResponseRedirect(reverse("user_profile", args=[author.username]))
    else:
        return render(request, "profile/unsubscribe.html", {"author": author})


@login_required
def delete_all_notifications(request):
    if request.method == "POST":
        Notification.objects.filter(user=request.user).delete()
        return redirect("notifications")


@login_required
def mark_as_viewed(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    if request.user == notification.user:
        notification.viewed = True
        notification.save()
        return redirect("notifications")
    else:
        return HttpResponseForbidden(
            "Вы не имеете прав на отметку этого уведомления как просмотренного."
        )


@login_required
def mark_all_as_viewed(request):
    notifications = Notification.objects.filter(user=request.user, viewed=False)
    notifications.update(viewed=True)
    return redirect("notifications")


@login_required
def subscribed_posts(request):
    subscriptions = Subscription.objects.filter(subscriber=request.user)
    subscribed_authors = [subscription.author for subscription in subscriptions]

    posts = []

    for author in subscribed_authors:
        author_posts = Post.objects.filter(author=author)
        posts.extend(author_posts)

    return render(request, "post/subscribed_posts.html", {"posts": posts})


@login_required
def subscriber_list(request, username):
    user = get_object_or_404(User, username=username)

    subscriptions = Subscription.objects.filter(author=user)

    return render(
        request,
        "profile/subscriber_list.html",
        {"user": user, "subscribers": subscriptions},
    )


@login_required
def toggle_favorite(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = request.user
    favorite, created = Favorite.objects.get_or_create(user=user, post=post)
    if not created:
        favorite.delete()
    return redirect("post_detail", pk=post_id)


@login_required
def favorite_posts(request):
    favorite_posts = Favorite.objects.filter(user=request.user).select_related("post")
    return render(
        request, "post/favorite_posts.html", {"favorite_posts": favorite_posts}
    )
