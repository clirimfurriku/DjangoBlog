from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Like(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.user} - {self.content_type}'


class Report(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    reviewed = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.user} - {self.content_type}'
