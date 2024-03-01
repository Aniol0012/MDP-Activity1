from django import forms
from posts.models import Comment
from posts.models import Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
