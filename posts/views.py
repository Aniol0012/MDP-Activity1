from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.db.models.functions import Substr
from django.db.models import Value as V
from django.db.models.functions import Concat
from posts.forms import CommentForm


def post_list(request):
    posts = Post.objects.all().annotate(short_content=Concat(
        Substr('content', 1, 200), V('...')))
    return render(request, 'posts/posts_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comment_set.all().order_by('-created_at')
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'posts/post_detail.html',
                  {'post': post, 'form': form, 'comments': comments})
