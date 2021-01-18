from typing import Union

from django import template

from blog.models import BlogPost, UserComment

register = template.Library()


@register.simple_tag
def has_user_liked(content: Union[BlogPost, UserComment], user) -> bool:
    return content.has_user_liked(user)
