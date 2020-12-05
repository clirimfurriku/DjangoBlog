from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from blog.models import BlogPost, UserComment, UserModel


class BlogPostsView(ListView):
    model = BlogPost
    template_name = "blog/posts.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pagination = context['page_obj']
        pages = []

        # Create a list of max 3 pages right and 3 pages left from the
        # current page and pas it to template as context argument
        for i in range(
                pagination.number - 3
                if pagination.number - 3 > 0 else 1,
                pagination.number + 3
                if pagination.number + 3 <= pagination.paginator.num_pages else pagination.paginator.num_pages + 1):
            pages.append(i)

        context['pages'] = pages
        return context


class AuthorPostsView(DetailView):
    model = UserModel
    template_name = 'blog/user_posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Only moderators or authors can have a articles page
        this_user = context['object']
        if this_user.user_type == 'm' or this_user.user_type == 'a':
            user_posts = BlogPost.objects.filter(author=this_user)
            context['posts'] = user_posts

        return context


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


class BloggersList(ListView):
    model = UserModel
    template_name = 'blog/authors.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        moderator_or_author = Q(user_type__exact='m') | Q(user_type__exact='a')
        return queryset.filter(moderator_or_author)
