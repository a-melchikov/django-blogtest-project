from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from subscriptions.models import Subscription
from services.paginators import GeneralPaginator
from services.blog_services import (
    get_filtered_posts,
    get_author_subscribers,
    handle_comment_form,
    get_user_posts,
    create_new_post,
)
from .models import Category, Post, Favorite
from .forms import PostForm, CommentForm


class BlogList(ListView):
    model = Post
    template_name = "home.html"
    context_object_name = "posts"
    paginate_by = 5
    ordering = "-publish_date"

    def get_queryset(self):
        return get_filtered_posts(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        paginator = GeneralPaginator(queryset, self.paginate_by)
        page_number = self.request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        context["posts"] = page_obj

        if self.request.user.is_authenticated:
            context["author_subscribers"] = get_author_subscribers(
                page_obj.object_list, self.request.user
            )

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

        if self.request.user.is_authenticated:
            context["is_favorite"] = post.favorite_set.filter(
                user=self.request.user
            ).exists()

        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            handle_comment_form(post, request.user, form)
            return HttpResponseRedirect(reverse("post_detail", args=[post.pk]))
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        post = self.get_object()
        user = self.request.user
        if not post.for_subscribers:
            return True
        return (
            post.author == user
            or user.subscriptions.filter(author=post.author).exists()
        )

    def handle_no_permission(self):
        post = self.get_object()
        return redirect("subscription_confirmation", post_id=post.pk)


class AboutPageView(TemplateView):
    template_name = "about.html"


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            create_new_post(form, request.user)
            return redirect("home")
    else:
        form = PostForm()
    categories = Category.objects.all()
    return render(
        request, "post/create_post.html", {"form": form, "categories": categories}
    )


@login_required
def my_posts(request):
    user_posts = get_user_posts(request.user)
    paginator = GeneralPaginator(user_posts)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "post/my_posts.html", {"page_obj": page_obj})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        raise Http404("Вы не имеете прав на редактирование данного поста")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.for_subscribers = request.POST.get("for_subscribers") == "on"
            post.save()
            form.save_m2m()
            return redirect("my_posts")
    else:
        form = PostForm(instance=post)

    selected_categories = post.categories.all()
    categories = Category.objects.all()
    for_subscribers = post.for_subscribers

    return render(
        request,
        "post/edit_post.html",
        {
            "form": form,
            "categories": categories,
            "selected_categories": selected_categories,
            "for_subscribers": for_subscribers,
        },
    )


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("my_posts")
    template_name = "post/post_confirm_delete.html"

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return get_object_or_404(Post, pk=post.pk)


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(categories=category).order_by("-publish_date")
    if request.user.is_authenticated:
        subscribed_authors = request.user.subscriptions.values_list(
            "author__id", flat=True
        )
        posts = posts.filter(
            Q(for_subscribers=False)
            | Q(author__id__in=subscribed_authors)
            | Q(author=request.user)
        )
    else:
        posts = posts.filter(for_subscribers=False)

    paginator = GeneralPaginator(posts)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "post/category_posts.html",
        {"category": category, "page_obj": page_obj},
    )


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

    if request.user.is_authenticated:
        subscribed_authors = request.user.subscriptions.values_list(
            "author__id", flat=True
        )
        posts = posts.filter(
            Q(for_subscribers=False)
            | Q(author__id__in=subscribed_authors)
            | Q(author=request.user)
        )
    else:
        posts = posts.filter(for_subscribers=False)

    paginator = GeneralPaginator(posts)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "search_results.html", {"page_obj": page_obj})


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


def subscribed_posts(request):
    subscriptions = Subscription.objects.filter(subscriber=request.user)
    subscribed_authors = [subscription.author for subscription in subscriptions]

    query = request.GET.get("query")
    all_posts = []

    for author in subscribed_authors:
        author_posts = Post.objects.filter(author=author)
        if query:
            author_posts = author_posts.filter(
                Q(title__icontains=query)
                | Q(body__icontains=query)
                | Q(author__username__icontains=query)
            )

        all_posts.extend(author_posts)

    all_posts_sorted = sorted(all_posts, key=lambda x: x.publish_date, reverse=True)

    paginator = GeneralPaginator(all_posts_sorted)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    author_subscribers = {}
    if request.user.is_authenticated:
        authors = {post.author_id: post.author for post in page_obj.object_list}
        author_subscribers = {
            author_id: list(
                User.objects.filter(
                    subscriptions__subscriber=request.user, id=author_id
                )
            )
            for author_id in authors.keys()
        }

    return render(
        request,
        "post/subscribed_posts.html",
        {"page_obj": page_obj, "author_subscribers": author_subscribers},
    )


@login_required
def toggle_favorite(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    favorite, created = Favorite.objects.get_or_create(user=user, post=post)
    if not created:
        favorite.delete()
    return redirect("post_detail", pk=post_id)


@login_required
def favorite_posts(request):
    favorite_posts = Favorite.objects.filter(user=request.user).select_related("post")
    paginator = GeneralPaginator(favorite_posts)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "post/favorite_posts.html", {"page_obj": page_obj})
