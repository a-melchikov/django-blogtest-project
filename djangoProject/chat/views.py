from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import MessageForm

class ChatPageView(TemplateView):
    template_name = "chat/chat.html"

def chat_view(request, room_name=None):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            print(message)
            form = MessageForm()
    else:
        form = MessageForm()
        
    messages = []

    return render(request, 'chat/chat.html', {'form': form, 'messages': messages, 'room_name': room_name})
