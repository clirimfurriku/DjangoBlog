from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from interaction.models import Like
from blog.models import BlogPost


@method_decorator(csrf_exempt, name='dispatch')
def like_post(request, post_id, *args, **kwargs):
    if request.method == "PUT":
        blog_post = BlogPost.objects.get(id=post_id)
        if not blog_post:
            raise Http404()
        # If user already liked the post remove the like

        if liked_obj := blog_post.likes.first():
            liked_obj.delete()
            return JsonResponse({"success": "true", "status": "unliked"})
        # If user has not liked the post add the like
        else:
            Like(user=request.user, content_object=blog_post).save()
            return JsonResponse({"success": "true", "status": "liked"})
    raise Http404
