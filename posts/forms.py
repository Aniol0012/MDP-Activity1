from django import forms
from posts.models import Comment
from posts.models import Post


class CommentForm(forms.ModelForm):
    """Form to create a new comment."""
    class Meta:
        model = Comment
        fields = ['content']


class PostForm(forms.ModelForm):
    """Form to create a new post."""
    class Meta:
        model = Post
        fields: str = ['title', 'content']
