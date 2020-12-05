from django.urls import path
from blog.views import BlogPostsView, BlogPostDetailView, AuthorPostsView, BloggersList

urlpatterns = [
    path('', BlogPostsView.as_view(), name="home"),
    path('blog/', BlogPostsView.as_view(), name="homeblog"),
    path('blog/<int:pk>', BlogPostDetailView.as_view(), name="post"),
    path('author/<int:pk>', AuthorPostsView.as_view(), name="author"),
    path('bloggers/', BloggersList.as_view(), name="bloggers"),
]
