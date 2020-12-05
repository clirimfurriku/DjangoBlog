from django.urls import path
from blog import views


urlpatterns = [
    path('', views.BlogPostsView.as_view(), name="home"),
    path('blog/', views.BlogPostsView.as_view(), name="homeblog"),
    path('blog/<int:pk>', views.BlogPostDetailView.as_view(), name="post"),
    path('author/<int:pk>', views.AuthorPostsView.as_view(), name="author"),
    path('bloggers/', views.BloggersList.as_view(), name="bloggers"),
    path('account/login/', views.UserLoginView.as_view(), name="login"),
    path('account/signup/', views.UserSignUpView.as_view(), name="login"),
]
