from library.models import Libro, Review
from django import forms

class BookForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['title', 'author', 'genre', 'pages']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'score']
