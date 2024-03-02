from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


class Post(models.Model):
    title = models.CharField(max_length=70, blank=False, null=False)
    content = models.TextField(max_length=2000, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def content_html(self):
        return mark_safe(self.content)


class Comment(models.Model):
    content = models.TextField(max_length=500, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'Liked by {self.user.username} on {self.post.title}'
