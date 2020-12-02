from django.db import models
from django.utils import timezone


class BlogPost(models.Model):
    title = models.CharField(max_length=256)
    short_description = models.CharField(max_length=1024)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    updated_date = models.DateTimeField(default=timezone.now())
    thumbnail_image = models.ImageField(null=True)

    def publish(self):
        self.created_date = timezone.now()
        self.updated_date = timezone.now()
        self.save()

    def update(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return f'{self.title} {self.updated_date}'


