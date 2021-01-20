from typing import Union, Type

from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from interaction.models import Like, Report
from blog.models import BlogPost, UserComment


def process_like_request(request, obj: Union[Type[BlogPost], Type[UserComment]], obj_id) -> JsonResponse:
    # if user is not authenticated or the method is not PUT
    # raise a Http404 error
    if not (request.user.is_authenticated or request.method == "PUT"):
        raise Http404()

    # if the database object does not exist raise Http404 error
    db_obj = obj.objects.get(id=obj_id)
    if not db_obj:
        raise Http404()

    # If user already liked the the object remove the like
    if liked_obj := db_obj.likes.filter(user=request.user):
        liked_obj.delete()
        return JsonResponse({"success": "true", "status": "unliked"})

    # If user has not liked the object add the like
    else:
        Like(user=request.user, content_object=db_obj).save()
        return JsonResponse({"success": "true", "status": "liked"})


def process_report_request(request, obj: Union[Type[BlogPost], Type[UserComment]], obj_id) -> JsonResponse:
    # if user is not authenticated or the method is not PUT
    # raise a Http404 error
    if not (request.user.is_authenticated or request.method == "PUT"):
        raise Http404()

    # if the database object does not exist raise Http404 error
    db_obj = obj.objects.get(id=obj_id)
    if not db_obj:
        raise Http404()

    # If user already reported the the object return a message
    if db_obj.reports.filter(user=request.user):
        return JsonResponse({"success": "true", "status": "exists"})

    # If user is reporting for the first time this object, add the report
    else:
        Report(user=request.user, content_object=db_obj).save()
        return JsonResponse({"success": "true", "status": "reported"})


@method_decorator(csrf_exempt, name='dispatch')
def like_post(request, post_id, *args, **kwargs):
    return process_like_request(request, BlogPost, post_id)


@method_decorator(csrf_exempt, name='dispatch')
def like_comment(request, comment_id, *args, **kwargs):
    return process_like_request(request, UserComment, comment_id)


@method_decorator(csrf_exempt, name='dispatch')
def report_post(request, post_id, *args, **kwargs):
    return process_report_request(request, BlogPost, post_id)


@method_decorator(csrf_exempt, name='dispatch')
def report_comment(request, comment_id, *args, **kwargs):
    return process_report_request(request, UserComment, comment_id)
