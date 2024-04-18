from django import forms
from .models import ChatRoom


class MessageForm(forms.Form):
    message = forms.CharField(label="Сообщение")


class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ["name"]
