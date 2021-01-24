from account.models import UserModel
from django.test import TestCase, Client
from django.urls import reverse

from blog.models import BlogPost, UserComment


class TestViews(TestCase):
    def setUp(self):
        self.Client = Client()

        self.blog_post = BlogPost.objects.create(
            title="Test Blog Post",
            short_description="Test Blog Post description",
            content="Test Blog Post content",
        )

        self.user_reader = UserModel.objects.create(
            email="user@example.com",
            username="test",
            user_type="r"
        )

        self.home_url = reverse('blog:home')
        self.search_url = reverse('blog:search')
        self.post_detail_url = reverse('blog:post', args=(self.blog_post.id,))

    def test_blog_posts_list(self):
        response = self.Client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogpost_list.html')

    def test_blog_posts_detail_list(self):
        response = self.Client.get(self.post_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogpost_detail.html')

    def test_user_can_comment(self):
        self.client.force_login(self.user_reader)
        response = self.client.post(self.post_detail_url, {
            'comment': 'Hey, this is a test comment'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(UserComment.objects.first().comment, 'Hey, this is a test comment')

    def test_search(self):
        response = self.client.get(self.search_url + '?q=' + self.blog_post.title)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.blog_post.title, response.content.decode('utf-8'))
