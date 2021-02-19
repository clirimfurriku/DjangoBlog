from django import template

from blog.models import BlogPost, UserComment

register = template.Library()


@register.simple_tag
def get_similar_posts(post: BlogPost) -> BlogPost:
    """Get a list of post sorted based of likes on the same category where the post is"""
    return BlogPost.objects.filter(category=post.category.first(), banned=False).exclude(id=post.id).order_by('likes')[:3]
