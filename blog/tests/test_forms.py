from django.test import SimpleTestCase

from blog.forms import PostForm


class TestForms(SimpleTestCase):
    def test_new_post_is_valid(self):
        form = PostForm(data={
            "title": "test post",
            "short_description": "test post description",
            "content": "test post content",
        })
        self.assertTrue(form.is_valid())

    def test_new_post_is_not_valid(self):
        form = PostForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
