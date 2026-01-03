from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Tag


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class TagWidget(forms.TextInput):
    def __init__(self, attrs=None):
        default_attrs = {
            'placeholder': 'Enter tags separated by commas'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

        
    def save(self, commit=True):
        post = super().save(commit=False)

        if commit:
            post.save()

        tag_names = self.cleaned_data.get('tags')

        if tag_names:
            tag_list = [name.strip() for name in tag_names.split(',')]
            tags = []

            for name in tag_list:
                tag, created = Tag.objects.get_or_create(name=name)
                tags.append(tag)

            post.tags.set(tags)

        return post

class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False)
    class Meta:
        model = Post
        fields = ['title', 'content','tags']
        widgets = {
            'tags': TagWidget()
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  





