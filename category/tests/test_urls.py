from django.test import SimpleTestCase
from django.urls import reverse, resolve

from category.views import CategoryPostsView, CategoryView


class TestUrls(SimpleTestCase):
    def test_category_posts_lists_is_resolved(self):
        url = reverse('category:category', args=('1',))
        self.assertEqual(resolve(url).func.view_class, CategoryPostsView)

    def test_categories_lists_is_resolved(self):
        url = reverse('category:categories')
        self.assertEqual(resolve(url).func.view_class, CategoryView)
