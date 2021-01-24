from account.models import UserModel
from django.test import TestCase, Client
from django.urls import reverse

from blog.models import BlogPost, UserComment
from category.models import Category


class TestViews(TestCase):
    def setUp(self):
        self.Client = Client()

        self.category = Category.objects.create(
            name="default category"
        )

        self.blog_post = BlogPost.objects.create(
            title="Test Blog Post",
            short_description="Test Blog Post description",
            content="Test Blog Post content",
        )

        self.blog_post_no_category = BlogPost.objects.create(
            title="Test Blog Post without category",
            short_description="Test Blog Post without category description",
            content="Test Blog Post without Category content",
        )

        self.blog_post.category.add(self.category)

        self.category_detail_url = reverse('category:category', args=(self.category.id,))
        self.category_list_url = reverse('category:categories')

    def test_category_list(self):
        response = self.Client.get(self.category_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category/category_list.html')
        self.assertIn(self.category.name, response.content.decode('utf-8'))

    def test_category_detail_list(self):
        response = self.Client.get(self.category_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogpost_list.html')
        self.assertIn(self.blog_post.title, response.content.decode('utf-8'))
        self.assertNotIn(self.blog_post_no_category.title, response.content.decode('utf-8'))
