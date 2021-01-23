from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from blog.models import BlogPost, UserComment, UserModel


class BlogPostsView(ListView):
    model = BlogPost
    queryset = BlogPost.objects.filter(banned=False).prefetch_related('category__parent', 'author')
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pagination = context['page_obj']
        pages = []

        # Create a list of max 3 pages right and 3 pages left from the
        # current page and pas it to template as context argument
        # If there is only one page do not include in pagination
        for i in range(
                pagination.number - 3
                if pagination.number - 3 > 0 else 1,
                pagination.number + 3
                if pagination.number + 3 <= pagination.paginator.num_pages else pagination.paginator.num_pages + 1):
            pages.append(i)

        context['pages'] = pages if len(pages) > 1 else []
        return context


class AuthorPostsView(DetailView):
    model = UserModel
    template_name = 'blog/components/user_posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.can_post:
            user_posts = BlogPost.objects.filter(author=self.object, banned=False)
            context['posts'] = user_posts
        else:
            raise Http404()
        return context


class BlogPostDetailView(DetailView):
    model = BlogPost
    queryset = BlogPost.objects.filter(banned=False).select_related('author').prefetch_related('author', 'likes')

    def post(self, request, *args, **kwargs):
        """
        Accept POST requests for this class
        DetailView does not include this by default
        """
        self.object = self.get_object()
        self.get_context_data(request=request, object=self.object)

        # Prevent user resubmit comment by refreshing the page
        return redirect(request.path)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            # If it is a post request check if there is a comment field
            # for current user and add it to the db
            comment = self.request.POST.get('comment')
            if comment:
                new_comment = UserComment(
                    author=self.request.user,
                    blog_post=self.object,
                    comment=comment
                )
                new_comment.save()
        comments = UserComment.objects.filter(blog_post=self.object, banned=False)
        if comments:
            context['comments'] = comments
        return context


class BloggersList(ListView):
    model = UserModel
    template_name = 'blog/authors_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        moderator_or_author = Q(user_type__in='a') | Q(user_type__in='s')
        return queryset.filter(moderator_or_author)


class BlogSearchView(ListView):
    model = BlogPost
    queryset = BlogPost.objects.filter(banned=False)
    template_name = 'blog/blogpost_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if not query:
            raise Http404
        search_query = Q(title__icontains=query) | Q(content__icontains=query)
        return queryset.filter(search_query, banned=False)
