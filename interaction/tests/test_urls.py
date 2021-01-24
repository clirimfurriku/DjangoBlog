from django.test import SimpleTestCase
from django.urls import reverse, resolve
from interaction.views import ban_post, like_post, ban_comment, like_comment, report_post, report_comment, \
    ReportedPosts, ReportedComments, ignore_reports_post, ignore_reports_comment


class TestUrls(SimpleTestCase):
    def test_reported_posts_is_resolved(self):
        url = reverse('interaction:reported_posts')
        self.assertEqual(resolve(url).func.view_class, ReportedPosts)

    def test_reported_comments_is_resolved(self):
        url = reverse('interaction:reported_comments')
        self.assertEqual(resolve(url).func.view_class, ReportedComments)

    def test_like_post_is_resolved(self):
        url = reverse('interaction:like_post', args=('1',))
        self.assertEqual(resolve(url).func, like_post)

    def test_like_comment_is_resolved(self):
        url = reverse('interaction:like_comment', args=('1',))
        self.assertEqual(resolve(url).func, like_comment)

    def test_report_post_is_resolved(self):
        url = reverse('interaction:report_post', args=('1',))
        self.assertEqual(resolve(url).func, report_post)

    def test_report_comment_is_resolved(self):
        url = reverse('interaction:report_comment', args=('1',))
        self.assertEqual(resolve(url).func, report_comment)

    def test_accept_reports_for_posts_is_resolved(self):
        url = reverse('interaction:accept_report_post', args=('1',))
        self.assertEqual(resolve(url).func, ignore_reports_post)

    def test_accept_reports_for_comments_is_resolved(self):
        url = reverse('interaction:accept_report_comment', args=('1',))
        self.assertEqual(resolve(url).func, ignore_reports_comment)

    def test_ban_post_is_resolved(self):
        url = reverse('interaction:ban_report_post', args=('1',))
        self.assertEqual(resolve(url).func, ban_post)

    def test_ban_comment_is_resolved(self):
        url = reverse('interaction:ban_report_comment', args=('1',))
        self.assertEqual(resolve(url).func, ban_comment)
