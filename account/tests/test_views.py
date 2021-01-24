from account.models import UserModel
from django.test import TestCase, Client
from django.urls import reverse

from blog.models import BlogPost


class TestViews(TestCase):
    def setUp(self):
        self.Client = Client()

        self.user_reader = UserModel.objects.create(
            email="user@example.com",
            username="test",
            user_type="r"
        )

        self.user_admin = UserModel.objects.create(
            email="user_admin@example.com",
            username="test_admin",
            user_type="s"
        )

        self.blog_post = BlogPost.objects.create(
            title="Test Blog Post",
            short_description="Test Blog Post description",
            content="Test Blog Post content",
            author=self.user_admin
        )

        self.blog_post_without_author = BlogPost.objects.create(
            title="Test Blog Post not by user",
            short_description="Test Blog Post not by user description",
            content="Test Blog Post not by user content",
        )

        self.account = reverse('account:account')
        self.login_url = reverse('account:login')
        self.logout_url = reverse('account:logout')
        self.signup_url = reverse('account:signup')

    def test_user_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_user_logout_view(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/logout.html')

    def test_user_logout_view_with_loggedin_account(self):
        self.client.force_login(self.user_reader)
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/logout.html')

    def test_user_signup_view(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')

    def test_user_signup_view_with_loggedin_user(self):
        self.client.force_login(self.user_reader)
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 302)

    def test_new_post_button_available_to_blogger_or_admins(self):
        self.client.force_login(self.user_admin)
        response = self.client.get(self.account)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/account_blogger.html')
        self.assertIn('New Post', response.content.decode('utf-8'))

    def test_new_post_button_not_available_to_readers(self):
        self.client.force_login(self.user_reader)
        response = self.client.get(self.account)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/usermodel_detail.html')
        self.assertNotIn('New Post', response.content.decode('utf-8'))

    def test_posts_show_in_user_account(self):
        self.client.force_login(self.user_admin)
        response = self.client.get(self.account)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.blog_post.title, response.content.decode('utf-8'))
        self.assertNotIn(self.blog_post_without_author.title, response.content.decode('utf-8'))
