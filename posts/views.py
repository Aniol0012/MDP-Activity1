from django.shortcuts import render, get_object_or_404
from .models import Post
from django.db.models.functions import Substr
from django.db.models import Value as V
from django.db.models.functions import Concat


def post_list(request):
    posts = Post.objects.all().annotate(short_content=Concat(
        Substr('content', 1, 200), V('...')))
    return render(request, 'posts/posts_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})
