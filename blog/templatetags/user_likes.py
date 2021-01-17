from django import template

from blog.models import BlogPost

register = template.Library()


@register.simple_tag
def has_user_liked(post: BlogPost, user) -> bool:
    return post.has_user_liked(user)
