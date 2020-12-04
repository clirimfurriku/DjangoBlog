from django.views.generic import ListView, DetailView

from blog.models import BlogPost


class BlogPostsView(ListView):
    model = BlogPost
    template_name = "blog/posts.html"


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/post.html"
