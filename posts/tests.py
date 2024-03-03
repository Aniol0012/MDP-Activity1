from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from posts.models import Post, Like


class PostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')
        self.post = Post.objects.create(title='Test Post',
                                        content='This is a test post.',
                                        author=self.user)

    def test_post_creation(self):
        self.assertEqual(self.post.title,
                         'Test Post')
        self.assertEqual(self.post.content,
                         'This is a test post.')
        self.assertEqual(self.post.author, self.user)

    def test_like_post(self):
        self.client.login(username='testuser',
                          password='12345')
        response = self.client.post(reverse('like_post',
                                            args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Like.objects.filter(user=self.user,
                                            post=self.post).exists())

    def test_post_list_view(self):
        response = self.client.get(reverse('posts_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertTemplateUsed(response,
                                'posts/posts_list.html')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail',
                                           args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertTemplateUsed(response, 'posts/post_detail.html')

    def test_post_create_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('post_create'),
                                    {'title': 'New Post',
                                     'content': 'This is a new post.'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='New Post',
                                            content='This is a new post.')
                        .exists())
