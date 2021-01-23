from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from account.models import UserModel
from category.models import Category
from interaction.models import Like, Report


class BlogPost(models.Model):
    title = models.CharField(max_length=256)
    short_description = models.TextField(max_length=1024)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    thumbnail_image = models.ImageField(null=True, blank=True)
    author = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ManyToManyField(Category, related_name='posts', blank=True)
    banned = models.BooleanField(default=False)
    likes = GenericRelation(Like)
    reports = GenericRelation(Report)

    class Meta:
        ordering = ['-created_date']

    def has_user_liked(self, user: UserModel):
        return self.likes.filter(user=user).exists()

    def ban(self):
        """Ban the post and automatically make all reports for this post as approved and reviewed"""
        self.reports.all().update(reviewed=True, approved=True)
        self.banned = True
        self.save()

    def remove_reports(self):
        """Mark all reports of this post as reviewed, but not approved"""
        self.reports.all().update(reviewed=True, approved=False)

    @property
    def like_count(self):
        return len(self.likes.all())

    @property
    def report_count(self):
        return len(self.reports.all())

    def __str__(self):
        return f'{self.title} {self.updated_date}'


class UserComment(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    comment = models.CharField(max_length=512)
    comment_date = models.DateTimeField(auto_now_add=True)
    banned = models.BooleanField(default=False)
    likes = GenericRelation(Like)
    reports = GenericRelation(Report)

    def has_user_liked(self, user: UserModel):
        return self.likes.filter(user=user).exists()

    def ban(self):
        """Ban the comment and automatically make all reports for this post as approved and reviewed"""
        self.reports.all().update(reviewed=True, approved=True)
        self.banned = True
        self.save()

    def remove_reports(self):
        """Mark all reports of this comment as reviewed, but not approved"""
        self.reports.all().update(reviewed=True, approved=False)

    @property
    def like_count(self):
        return len(self.likes.all())

    @property
    def report_count(self):
        return len(self.reports.all())

    def __str__(self):
        return f'{self.author} {self.comment_date}'
