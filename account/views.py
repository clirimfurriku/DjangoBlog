from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import DetailView, CreateView, UpdateView

from blog.forms import PostForm
from blog.models import BlogPost, UserModel
from account.forms import SignUpForm


class MyAccount(DetailView):
    model = UserModel

    def get_object(self, queryset=None):
        if not self.request.user.is_authenticated:
            raise Http404()
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add context data for posts made by the user
        if self.object.can_post:
            user_posts = BlogPost.objects.filter(author=self.object)
            context['posts'] = user_posts

        return context


class UserLoginView(LoginView):
    template_name = 'account/login.html'

    def get(self, request, **kwargs):
        # If user already logged in redirect home
        if request.user.is_authenticated:
            return redirect('blog:home')
        return super().get(request, **kwargs)


class UserLogoutView(LogoutView):
    template_name = 'account/logout.html'


class UserSignUpView(CreateView):
    template_name = 'account/signup.html'
    success_url = '/'
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blog:home')
        return super(UserSignUpView, self).get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            return self.form_invalid(form)
        self.object = form.save()
        login(request, self.object)
        return redirect('blog:home')


class MakePostView(LoginRequiredMixin, CreateView):
    template_name = 'account/post.html'
    success_url = '/'
    form_class = PostForm

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.can_post:
            # Only logged in Authors and Moderators can post
            raise Http404("Page not found")
        return super(MakePostView, self).get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.can_post:
            # Only logged in Authors and Moderators can post
            raise Http404("Page not found")

        form = self.get_form()
        if not form.is_valid():
            return self.form_invalid(form)
        self.object = form.save()
        self.object.author = request.user
        self.object.save()
        return redirect('blog:home')


class UpdateProfile(UpdateView):
    model = UserModel
    fields = ['bio', 'twitter', 'instagram', 'facebook', 'avatar']
    template_name = 'account/update_profile.html'
    success_url = '/account'

    def get_object(self, queryset=None):
        if not self.request.user.is_authenticated:
            raise Http404()
        return self.request.user
