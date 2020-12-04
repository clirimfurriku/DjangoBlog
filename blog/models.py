from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


class UserModel(models.Model):
    # There will be three types of users:
    # 1 - Moderator (Can publish articles, edit, comment)
    # 2 - Authors (Can publish articles, comment)
    # 3 - Reader (Can comment on articles)
    user_type = models.CharField(
        max_length=1,
        choices=(
            ('m', 'Author'),
            ('a', 'Author'),
            ('r', 'Reader')
        ),
        null=True,
        blank=True
    )
    bio = models.CharField(max_length=2048, null=True, blank=True)
    # Social profiles
    twitter = models.CharField(max_length=128, null=True, blank=True)
    instagram = models.CharField(max_length=128, null=True, blank=True)
    facebook = models.CharField(max_length=128, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)  # profile pic

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username if self.user else "Unknown"}'


class BlogPost(models.Model):
    title = models.CharField(max_length=256)
    short_description = models.TextField(max_length=1024)
    content = models.TextField()  # TODO: Check if html i supported
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    thumbnail_image = models.ImageField(null=True, blank=True)
    author = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.title} {self.updated_date}'


class UserComment(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    comment = models.CharField(max_length=512)
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} {self.comment_date}'
