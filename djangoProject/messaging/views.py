from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from authentication.models import Profile
from services.paginators import GeneralPaginator
from services.messaging_services import (
    get_messages_for_user,
    get_sent_messages_for_user,
    get_user_suggestions_by_text,
    send_message_from_user_to_user,
)


@login_required
def inbox(request):
    filter_name = request.GET.get("filter_name")
    messages = get_messages_for_user(request.user, filter_name)
    page_number = request.GET.get("page", 1)
    paginator = GeneralPaginator(messages)
    page_obj = paginator.get_page(page_number)
    return render(request, "messages/inbox.html", {"page_obj": page_obj})


@login_required
def send_message(request):
    if request.method == "POST":
        recipient = request.POST["recipient"]
        subject = request.POST["subject"]
        body = request.POST["body"]
        send_message_from_user_to_user(request.user, recipient, subject, body)
        return redirect("inbox")
    else:
        profiles = Profile.objects.all()
        return render(request, "messages/send_message.html", {"profiles": profiles})


@login_required
def get_user_suggestions(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        input_text = request.GET.get("input_text", None)
        if input_text:
            suggestions = get_user_suggestions_by_text(input_text)
            return JsonResponse(suggestions, safe=False)
    return JsonResponse({}, status=400)


@login_required
def sent_messages(request):
    messages = get_sent_messages_for_user(request.user)
    page_number = request.GET.get("page", 1)
    paginator = GeneralPaginator(messages)
    page_obj = paginator.get_page(page_number)
    return render(request, "messages/sent_messages.html", {"page_obj": page_obj})
