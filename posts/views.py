from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.db.models.functions import Substr
from django.db.models import Value as V
from django.db.models.functions import Concat
from posts.forms import CommentForm, PostForm, SignUpForm
from django.contrib import messages
from posts import utils as u


def post_list(request):
    """Show the list of posts."""
    posts = Post.objects.all().annotate(short_content=Concat(
        Substr('content', 1, 200), V('...')))
    return render(request, 'posts/posts_list.html', {'posts': posts})


def post_detail(request, pk):
    """Show the details of a post."""
    post = get_object_or_404(Post, pk=pk)
    order: str = request.GET.get('order', 'desc')
    comments = post.comment_set.all().order_by(
        f'{"-" if order == "desc" else ""}created_at')
    if request.method == "POST":
        if u.is_not_authenticated(request):
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
    if u.is_not_authenticated(request):
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
    if u.is_author(post, request) or u.is_superuser(request):
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
    else:
        messages.error(request, "You don't have permission to edit this post.")
        return redirect('post_detail', pk=post.pk)


def post_delete(request, pk):
    """Delete a post."""
    post = get_object_or_404(Post, pk=pk)
    if u.is_author(post, request) or u.is_superuser(request):
        post.delete()
        if u.is_superuser(request):
            messages.info(request, "Post id " + str(pk) + " has been deleted.")
        else:
            messages.info(request, "Post has been deleted.")
        return redirect('posts_list')
    else:
        messages.error(request,
                       "You don't have permission to delete this post.")
        return redirect('post_detail', pk=post.pk)


def signup(request):
    """Sign up a new user."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def like_post(request, post_id: int):
    """Like a post."""
    if u.is_not_authenticated(request):
        return redirect('login')
    post = get_object_or_404(Post, pk=post_id)
    like, created = post.like_set.get_or_create(user=request.user)
    if not created:
        messages.info(request, 'You already liked this post.')
    return redirect(request.META.get('HTTP_REFERER', 'posts_list'))
