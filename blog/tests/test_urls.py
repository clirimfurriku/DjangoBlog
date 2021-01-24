from django.test import SimpleTestCase
from django.urls import reverse, resolve

from blog.views import BlogPostsView, BlogPostDetailView, AuthorPostsView, BlogSearchView, BloggersList


class TestUrls(SimpleTestCase):
    def test_blog_home_is_resolved(self):
        url = reverse('blog:home')
        self.assertEqual(resolve(url).func.view_class, BlogPostsView)

    def test_blog_homeposts_is_resolved(self):
        url = reverse('blog:home')
        self.assertEqual(resolve(url).func.view_class, BlogPostsView)

    def test_blog_post_detail_is_resolved(self):
        url = reverse('blog:post', args=('1',))
        self.assertEqual(resolve(url).func.view_class, BlogPostDetailView)

    def test_blog_author_listposts_is_resolved(self):
        url = reverse('blog:author', args=('1',))
        self.assertEqual(resolve(url).func.view_class, AuthorPostsView)

    def test_blog_search_page_is_resolved(self):
        url = reverse('blog:search')
        self.assertEqual(resolve(url).func.view_class, BlogSearchView)

    def test_bloggers_list_is_resolved(self):
        url = reverse('blog:bloggers')
        self.assertEqual(resolve(url).func.view_class, BloggersList)
