from django.urls import path

from blog import views as blog_views

app_name = 'blog'

urlpatterns = [
    path('', blog_views.BlogPostsView.as_view(), name="home"),
    path('blog/', blog_views.BlogPostsView.as_view(), name="homeblog"),
    path('blog/<int:pk>', blog_views.BlogPostDetailView.as_view(), name="post"),
    path('author/<int:pk>', blog_views.AuthorPostsView.as_view(), name="author"),
    path('search/', blog_views.BlogSearchView.as_view(), name="search"),
    path('bloggers/', blog_views.BloggersList.as_view(), name="bloggers"),
]
