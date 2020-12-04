from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from blog.models import BlogPost, UserComment, UserModel


class BlogPostsView(ListView):
    model = BlogPost
    template_name = "blog/posts.html"


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/post.html"

    def post(self, request, *args, **kwargs):
        """
        Accept POST requests for this class
        DetailView does not include this by default
        """
        self.object = self.get_object()
        context = self.get_context_data(request=request, object=self.object)
        if request.method == "POST":
            # Prevent user resubmit comment by refreshing the page
            return redirect(request.path)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            # If it is a post request check if there is a comment field
            # for current user and add it to the db
            comment = self.request.POST.get('comment')
            if comment is not None:
                new_comment = UserComment(
                    author=UserModel.objects.get(user=kwargs.get('request').user),
                    blog_post=context['object'],
                    comment=comment
                )
                new_comment.save()
        comments = UserComment.objects.filter(blog_post=context.get('object'))
        if comments:
            context['comments'] = comments
        return context
