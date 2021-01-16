from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='child')

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    @property
    def get_post_count(self):
        posts = self.posts.count()
        for child in self.child.all():
            posts += child.posts.count()
        return posts
