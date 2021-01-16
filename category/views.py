from django.views.generic import ListView, DetailView

from blog.models import BlogPost
from category.models import Category


class CategoryView(ListView):
    model = Category


class CategoryPostsView(DetailView):
    model = Category
    template_name = 'blog/blogpost_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_posts = BlogPost.objects.filter(category=self.object)
        if blog_posts:
            context['object_list'] = blog_posts
        return context
