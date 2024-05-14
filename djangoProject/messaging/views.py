from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from authentication.models import Profile
from notifications.models import Notification
from .models import Message


@login_required
def inbox(request):
    filter_name = request.GET.get("filter_name")

    messages = Message.objects.filter(recipient=request.user).order_by("-timestamp")

    if filter_name:
        messages = messages.filter(sender__username=filter_name)

    paginator = Paginator(messages, 5)
    page_number = request.GET.get("page")
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        "page_obj": page_obj,
    }
    return render(request, "messages/inbox.html", context)


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


def get_user_suggestions(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        input_text = request.GET.get("input_text", None)
        if input_text:
            users = User.objects.filter(username__icontains=input_text)[:5]
            suggestions = [user.username for user in users]
            return JsonResponse(suggestions, safe=False)
    return JsonResponse({}, status=400)
