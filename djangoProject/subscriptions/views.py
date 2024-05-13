from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User

from blog.models import Notification, Post
from .models import Subscription


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


class SubscriptionConfirmationView(TemplateView):
    template_name = "post/subscription_confirmation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs["post_id"]
        post = get_object_or_404(Post, pk=post_id)
        context["post"] = post
        context["post_id"] = post_id
        return context
