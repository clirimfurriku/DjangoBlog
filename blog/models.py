from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=256)
    short_description = models.CharField(max_length=1024)
    content = models.TextField()
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()
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


