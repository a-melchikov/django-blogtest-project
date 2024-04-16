from django import forms

from authentication.models import Profile
from .models import Comment, Post, Category


class PostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Post
        fields = ["title", "body", "categories"]


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
