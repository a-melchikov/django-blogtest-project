from django import forms

from authentication.models import Profile
from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["date_of_birth", "country", "city", "bio"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

    text = forms.CharField(
        label="Введите ваш комментарий:",
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )
