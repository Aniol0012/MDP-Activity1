# from django.test import TestCase
from posts.models import Post


# Create your tests here.

def test_post_creation(self):
    post = Post.objects.create(title='Test Post')
    self.assertEqual(post.title, 'Test Post')
    self.assertEqual(post.content, 'This is a test post.')
    self.assertEqual(post.__str__(), post.title)
    self.assertEqual(post.content_html(), post.content)


def test_post_list_view(self):
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'posts/posts_list.html')
    self.assertContains(response, 'Posts')


def test_post_detail_view(self):
    post = Post.objects.create(title='Test Post')
    response = self.client.get(f'/post/{post.pk}/')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'posts/post_detail.html')
    self.assertContains(response, post.title)
    self.assertContains(response, post.content)


def test_post_create_view(self):
    response = self.client.get('/post/create/')
    self.assertEqual(response.status_code, 302)
    self.client.login(username='tester', password='12345')
    response = self.client.get('/post/create/')
    self.assertEqual(response.status_code, 200)
    response = self.client.post('/post/create/', {'title': 'Test Post'})
    self.assertEqual(response.status_code, 302)
    self.assertEqual(Post.objects.count(), 1)
    post = Post.objects.first()
    self.assertEqual(post.title, 'Test Post')
    self.assertEqual(post.content, 'This is a test post.')
    self.assertEqual(post.author.username, 'tester')
    self.assertEqual(post.__str__(), post.title)
    self.assertEqual(post.content_html(), post.content)
