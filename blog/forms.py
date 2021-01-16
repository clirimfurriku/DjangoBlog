from django.forms import ModelForm

from blog.models import BlogPost


class PostForm(ModelForm):
    class Meta:
        model = BlogPost
        fields = (
            'title',
            'short_description',
            'content',
            'thumbnail_image',
            'category'
        )
