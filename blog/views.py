from django.views.generic import ListView, DetailView

from blog.models import BlogPost, UserComment


class BlogPostsView(ListView):
    model = BlogPost
    template_name = "blog/posts.html"


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = UserComment.objects.filter(blog_post=context.get('object'))
        if comments:
            context['comments'] = comments
        return context
