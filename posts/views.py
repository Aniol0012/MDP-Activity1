from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.db.models.functions import Substr
from django.db.models import Value as V
from django.db.models.functions import Concat
from posts.forms import CommentForm, PostForm, SignUpForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied


def post_list(request):
    """Show the list of posts."""
    posts = Post.objects.all().annotate(short_content=Concat(
        Substr('content', 1, 200), V('...')))
    return render(request, 'posts/posts_list.html', {'posts': posts})


def post_detail(request, pk):
    """Show the details of a post."""
    post = get_object_or_404(Post, pk=pk)
    order = request.GET.get('order', 'desc')
    comments = post.comment_set.all().order_by(
        f'{"-" if order == "desc" else ""}created_at')
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
    dark_mode = 'dark_mode' if 'dark_mode' in request.session else 'light_mode'
    return render(request, 'posts/post_detail.html',
                  {'post': post,
                   'form': form,
                   'comments': comments,
                   'theme': dark_mode})


def post_create(request):
    """Create a new post."""
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/post_create.html', {'form': form})


def dark_mode(request):
    """Enable dark mode."""
    if 'dark_mode' in request.session:
        del request.session['dark_mode']
    else:
        request.session['dark_mode'] = True
    return redirect(request.META.get('HTTP_REFERER', 'post_list'))


def post_edit(request, pk):
    """Edit a post."""
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author and not request.user.is_superuser:
        return redirect('post_detail', pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_edit.html',
                  {'form': form, 'post': post})


def post_delete(request, pk):
    """Delete a post."""
    post = get_object_or_404(Post, pk=pk)
    if (request.user == post.author) or request.user.is_superuser:
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('posts_list')
    else:
        raise PermissionDenied


def signup(request):
    """Sign up a new user."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def like_post(request, post_id):
    """Like a post."""
    if not request.user.is_authenticated:
        return redirect('login')
    post = get_object_or_404(Post, pk=post_id)
    post.like_set.get_or_create(user=request.user)
    return redirect(request.META.get('HTTP_REFERER', 'posts_list'))
