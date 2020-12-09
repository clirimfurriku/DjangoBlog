from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from blog.forms import SignUpForm, PostForm
from blog.models import BlogPost, UserComment, UserModel


class BlogPostsView(ListView):
    model = BlogPost
    template_name = "blog/posts.html"
    paginate_by = 6

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
    template_name = 'blog/components/user_posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Only moderators or authors can have a articles page
        this_user = self.object
        if this_user.user_type == 'm' or this_user.user_type == 'a':
            user_posts = BlogPost.objects.filter(author=this_user)
            context['posts'] = user_posts

        return context


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/single_post.html"

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
            if comment is not None:
                new_comment = UserComment(
                    author=self.request.user,
                    blog_post=self.object,
                    comment=comment
                )
                new_comment.save()
        comments = UserComment.objects.filter(blog_post=self.object)
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


class MyAccount(DetailView):
    model = UserModel
    template_name = 'blog/account/account.html'

    def get_object(self, queryset=None):
        if not self.request.user.is_authenticated:
            raise Http404()
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add context data for posts made by the user
        if self.object.user_type == 'm' or self.object.user_type == 'a':
            user_posts = BlogPost.objects.filter(author=self.object)
            context['posts'] = user_posts

        return context


class UserLoginView(LoginView):
    template_name = 'blog/account/login.html'

    def get(self, request, **kwargs):
        # If user already logged in redirect home
        if request.user.is_authenticated:
            return redirect('home')
        return super().get(request, **kwargs)


class UserLogoutView(LogoutView):
    template_name = 'blog/account/logout.html'


class UserSignUpView(CreateView):
    template_name = 'blog/account/signup.html'
    success_url = '/'
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super(UserSignUpView, self).get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.object = form.save()
            login(request, self.object)
            return redirect('home')
        else:
            return self.form_invalid(form)


class MakePostView(LoginRequiredMixin, CreateView):
    template_name = 'blog/account/post.html'
    success_url = '/'
    form_class = PostForm

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type == 'r':
            # Only logged in Authors and Moderators can post
            raise Http404("Page not found")
        return super(MakePostView, self).get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type == 'r':
            # Only logged in Authors and Moderators can post
            raise Http404("Page not found")

        form = self.get_form()
        if form.is_valid():
            self.object = form.save()
            self.object.author = request.user
            self.object.save()
            return redirect('home')
        else:
            return self.form_invalid(form)


class UpdateProfile(UpdateView):
    model = UserModel
    fields = ['bio', 'twitter', 'instagram', 'facebook', 'avatar']
    template_name = 'blog/account/update_profile.html'
    success_url = '/account'

    def get_object(self, queryset=None):
        if not self.request.user.is_authenticated:
            raise Http404()
        return self.request.user
