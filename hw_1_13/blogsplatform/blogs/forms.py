from django import forms
from django.forms import ModelForm
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')
        labels = {
            'title': 'Title',
            'content': 'Content'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {
            'content': 'Content'
        }
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }
