from django.urls import path
from account import views as blog_views
from django.contrib.auth import views as admin_views

app_name = 'account'

urlpatterns = [
    path('', blog_views.MyAccount.as_view(), name="account"),
    path('post/', blog_views.MakePostView.as_view(), name="new_post"),
    path('edit/', blog_views.UpdateProfile.as_view(), name="update_profile"),
    path('login/', blog_views.UserLoginView.as_view(), name="login"),
    path('logout/', blog_views.UserLogoutView.as_view(), name="logout"),
    path('signup/', blog_views.UserSignUpView.as_view(), name="signup"),
]

# Add password reset URLs from django admin
urlpatterns += [
    path('password_change/', admin_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', admin_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', admin_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', admin_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', admin_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', admin_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
