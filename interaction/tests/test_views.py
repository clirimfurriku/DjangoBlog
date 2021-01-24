from account.models import UserModel
from django.test import TestCase, Client
from django.urls import reverse

from blog.models import BlogPost, UserComment
from interaction.models import Report


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

        self.user_admin = UserModel.objects.create(
            email="user_admin@example.com",
            username="test_admin",
            user_type="s"
        )

        self.user_comment = UserComment.objects.create(
            author=self.user_reader,
            blog_post=self.blog_post,
            comment="Hey, this is a test comment",
        )

        self.like_post_url = reverse('interaction:like_comment', args=(self.blog_post.id,))
        self.like_comment_url = reverse('interaction:like_comment', args=(self.user_comment.id,))
        self.report_post_url = reverse('interaction:report_post', args=(self.user_comment.id,))
        self.report_comment_url = reverse('interaction:report_comment', args=(self.user_comment.id,))

        self.reported_posts_url = reverse('interaction:reported_posts')
        self.reported_comments_url = reverse('interaction:reported_comments')

        self.ban_reported_post_url = reverse('interaction:ban_report_post', args=(self.blog_post.id,))
        self.ban_reported_comment_url = reverse('interaction:ban_report_comment', args=(self.user_comment.id,))

        self.ignore_reports_post_url = reverse('interaction:accept_report_post', args=(self.blog_post.id,))
        self.ignore_reports_comment_url = reverse('interaction:accept_report_comment', args=(self.user_comment.id,))

    def test_like_blog_post(self):
        self.client.force_login(self.user_reader)
        response = self.client.put(self.like_post_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": "true", "status": "liked"})
        response = self.client.put(self.like_post_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": "true", "status": "unliked"})

    def test_like_blog_post_not_put_returns_404(self):
        self.client.force_login(self.user_reader)
        response = self.client.post(self.like_post_url)
        self.assertEqual(response.status_code, 404)
        response = self.client.get(self.like_post_url)
        self.assertEqual(response.status_code, 404)

    def test_like_comment_post(self):
        self.client.force_login(self.user_reader)
        response = self.client.put(self.like_comment_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": "true", "status": "liked"})
        response = self.client.put(self.like_comment_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": "true", "status": "unliked"})

    def test_like_comment_not_put_returns_404(self):
        self.client.force_login(self.user_reader)
        response = self.client.post(self.like_comment_url)
        self.assertEqual(response.status_code, 404)
        response = self.client.get(self.like_comment_url)
        self.assertEqual(response.status_code, 404)

    def test_report_post(self):
        self.client.force_login(self.user_reader)
        response = self.client.put(self.report_post_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": "true", "status": "reported"})
        response = self.client.put(self.report_post_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": "true", "status": "exists"})

    def test_report_comment(self):
        self.client.force_login(self.user_reader)
        response = self.client.put(self.report_comment_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": "true", "status": "reported"})
        response = self.client.put(self.report_comment_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": "true", "status": "exists"})

    def test_reported_posts_page(self):
        self.client.force_login(self.user_reader)
        response = self.client.put(self.report_post_url)
        self.assertEqual(response.status_code, 200)

        self.client.force_login(self.user_admin)
        response = self.client.get(self.reported_posts_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'interaction/reported_posts_list.html')
        self.assertIn(self.blog_post.title, response.content.decode('utf-8'))

    def test_only_staff_can_view_reported_posts(self):
        self.client.force_login(self.user_reader)
        response = self.client.put(self.report_post_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.reported_posts_url)
        self.assertEqual(response.status_code, 404)
        self.assertNotIn(self.blog_post.title, response.content.decode('utf-8'))

    def test_reported_comments_page(self):
        self.client.force_login(self.user_reader)
        response = self.client.put(self.report_comment_url)
        self.assertEqual(response.status_code, 200)

        self.client.force_login(self.user_admin)
        response = self.client.get(self.reported_comments_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'interaction/reported_comments_list.html')
        self.assertIn(self.blog_post.title, response.content.decode('utf-8'))

    def test_only_staff_can_view_reported_comments(self):
        self.client.force_login(self.user_reader)
        response = self.client.put(self.report_post_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.reported_posts_url)
        self.assertEqual(response.status_code, 404)
        self.assertNotIn(self.blog_post.title, response.content.decode('utf-8'))

    def test_banning_post(self):
        self.client.force_login(self.user_admin)
        response = self.client.put(self.report_post_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.put(self.ban_reported_post_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": "true", "status": "banned"})
        self.assertEqual(BlogPost.objects.first().banned, True)
        self.assertEqual(Report.objects.first().reviewed, True)
        self.assertEqual(Report.objects.first().approved, True)

    def test_banning_comment(self):
        self.client.force_login(self.user_admin)
        response = self.client.put(self.report_comment_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.put(self.ban_reported_comment_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": "true", "status": "banned"})
        self.assertEqual(UserComment.objects.first().banned, True)
        self.assertEqual(Report.objects.first().reviewed, True)
        self.assertEqual(Report.objects.first().approved, True)

    def test_ignoring_post_reports(self):
        self.client.force_login(self.user_admin)
        response = self.client.put(self.report_post_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.put(self.ignore_reports_post_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": "true", "status": "accepted"})
        self.assertEqual(BlogPost.objects.first().banned, False)
        self.assertEqual(Report.objects.first().reviewed, True)
        self.assertEqual(Report.objects.first().approved, False)

    def test_ignoring_comment_reports(self):
        self.client.force_login(self.user_admin)
        response = self.client.put(self.report_comment_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.put(self.ignore_reports_comment_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": "true", "status": "accepted"})
        self.assertEqual(UserComment.objects.first().banned, False)
        self.assertEqual(Report.objects.first().reviewed, True)
        self.assertEqual(Report.objects.first().approved, False)

    def test_non_staff_can_not_ban_posts(self):
        self.client.force_login(self.user_reader)
        response = self.client.put(self.report_post_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.put(self.ban_reported_post_url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(BlogPost.objects.first().banned, False)
        self.assertEqual(Report.objects.first().reviewed, False)
        self.assertEqual(Report.objects.first().approved, False)

    def test_non_staff_can_not_ban_comments(self):
        self.client.force_login(self.user_reader)
        response = self.client.put(self.report_comment_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.put(self.ban_reported_post_url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(UserComment.objects.first().banned, False)
        self.assertEqual(Report.objects.first().reviewed, False)
        self.assertEqual(Report.objects.first().approved, False)
