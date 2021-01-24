from unittest import TestCase

from django.test import SimpleTestCase

from account.forms import SignUpForm
from blog.forms import PostForm


class TestForms(TestCase):
    def test_new_signup_is_valid(self):
        form = SignUpForm(data={
            "username": "testaccount",
            "email": "test@example.com",
            "password1": "SecretPassword123",
            "password2": "SecretPassword123",
            "user_type": "a",
        })
        self.assertTrue(form.is_valid())

    def test_administrator_signup_not_allowed(self):
        form = SignUpForm(data={
            "username": "testaccount",
            "email": "test@example.com",
            "password1": "SecretPassword123",
            "password2": "SecretPassword123",
            "user_type": "s",
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_strong_password_required(self):
        form = SignUpForm(data={
            "username": "testaccount",
            "email": "test@example.com",
            "password1": "12345678",
            "password2": "12345678",
            "user_type": "a",
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_valid_email_required(self):
        form = SignUpForm(data={
            "username": "testaccount",
            "email": "invalid_email_test",
            "password1": "SecretPassword123",
            "password2": "SecretPassword123",
            "user_type": "a",
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_new_signup_is_not_valid(self):
        form = SignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)
