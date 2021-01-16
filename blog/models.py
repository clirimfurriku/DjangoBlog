from django.db import models
from django.utils import timezone
from account.models import UserModel
from category.models import Category


class BlogPost(models.Model):
    title = models.CharField(max_length=256)
    short_description = models.TextField(max_length=1024)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    thumbnail_image = models.ImageField(null=True, blank=True)
    author = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ManyToManyField(Category, related_name='posts', blank=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f'{self.title} {self.updated_date}'


class UserComment(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    comment = models.CharField(max_length=512)
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} {self.comment_date}'
