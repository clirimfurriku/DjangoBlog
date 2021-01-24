from django.test import SimpleTestCase
from django.urls import reverse, resolve

from account.views import MyAccount, MakePostView, UpdateProfile, UserLoginView, UserLogoutView, UserSignUpView


class TestUrls(SimpleTestCase):
    def test_account_details_is_resolved(self):
        url = reverse('account:account')
        self.assertEqual(resolve(url).func.view_class, MyAccount)

    def test_make_new_post_is_resolved(self):
        url = reverse('account:new_post')
        self.assertEqual(resolve(url).func.view_class, MakePostView)

    def test_edit_profile_is_resolved(self):
        url = reverse('account:update_profile')
        self.assertEqual(resolve(url).func.view_class, UpdateProfile)

    def test_login_page_is_resolved(self):
        url = reverse('account:login')
        self.assertEqual(resolve(url).func.view_class, UserLoginView)

    def test_logout_page_is_resolved(self):
        url = reverse('account:logout')
        self.assertEqual(resolve(url).func.view_class, UserLogoutView)

    def test_signup_page_is_resolved(self):
        url = reverse('account:signup')
        self.assertEqual(resolve(url).func.view_class, UserSignUpView)



