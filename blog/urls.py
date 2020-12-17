from django.urls import path
from blog import views as blog_views
from django.contrib.auth import views as admin_views

urlpatterns = [
    path('', blog_views.BlogPostsView.as_view(), name="home"),
    path('blog/', blog_views.BlogPostsView.as_view(), name="homeblog"),
    path('blog/<int:pk>', blog_views.BlogPostDetailView.as_view(), name="post"),
    path('author/<int:pk>', blog_views.AuthorPostsView.as_view(), name="author"),
    path('search/', blog_views.BlogSearchView.as_view(), name="search"),
    path('bloggers/', blog_views.BloggersList.as_view(), name="bloggers"),
    path('account/', blog_views.MyAccount.as_view(), name="account"),
    path('account/post/', blog_views.MakePostView.as_view(), name="newpost"),
    path('account/edit/', blog_views.UpdateProfile.as_view(), name="updateprofile"),
    path('account/login/', blog_views.UserLoginView.as_view(), name="login"),
    path('account/logout/', blog_views.UserLogoutView.as_view(), name="logout"),
    path('account/signup/', blog_views.UserSignUpView.as_view(), name="signup"),
]

# Add password reset URLs from django admin
urlpatterns += [
    path('account/password_change/', admin_views.PasswordChangeView.as_view(), name='password_change'),
    path('account/password_change/done/', admin_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('account/password_reset/', admin_views.PasswordResetView.as_view(), name='password_reset'),
    path('account/password_reset/done/', admin_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('account/reset/<uidb64>/<token>/', admin_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('account/reset/done/', admin_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
