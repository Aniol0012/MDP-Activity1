from django import forms
from posts.models import Comment
from posts.models import Post, User
from django.contrib.auth.forms import UserCreationForm


class CommentForm(forms.ModelForm):
    """Form to create a new comment."""
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'comment-input'}),
        label='Comment content'
    )

    class Meta:
        model = Comment
        fields = ['content']


class PostForm(forms.ModelForm):
    """Form to create a new post."""
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'content-style'}),
        label='Post content'
    )

    class Meta:
        model = Post
        fields: str = ['title', 'content']


class SignUpForm(UserCreationForm):
    """Form to create a new user."""
    email = forms.EmailField(max_length=254,
                             help_text='Required. Inform a valid '
                                       'email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
