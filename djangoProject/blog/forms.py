from django import forms

from authentication.models import Profile
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["date_of_birth", "country", "city", "bio"]
