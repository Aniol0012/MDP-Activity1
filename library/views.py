from django.shortcuts import render, redirect, get_object_or_404
from library.forms import BookForm, ReviewForm
from django.views.generic import ListView
from library.models import Libro


class BookListView(ListView):
    model = Libro
    template_name = 'book_list.html'
    context_object_name = 'books'


def book_detail(request, pk):
    book = get_object_or_404(Libro, pk=pk)
    return render(request, 'detail_book.html', {'book': book})


def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            # Redirigir al usuario a detalles del libro
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
        return render(request, 'create_book.html', {'form': form})


def create_review(request, pk):
    book = get_object_or_404(Libro, id=pk)
    # lo mismo que book = Libro.objects.get(id=pk) pero con
    # control de fallos si no lo encuentra.
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('book_detail', pk=book.id)
    else:
        form = ReviewForm()
        return render(request, 'create_review.html',
                      {'form': form, 'book': book})
