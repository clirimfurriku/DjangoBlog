from typing import Union, Type

from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from interaction.models import Like, Report
from blog.models import BlogPost, UserComment


def process_like_request(request, obj: Union[Type[BlogPost], Type[UserComment]], obj_id) -> JsonResponse:
    # if user is not authenticated or the method is not PUT
    # raise a Http404 error
    if not request.user.is_authenticated or not request.method == "PUT":
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
    if not request.user.is_authenticated or not request.method == "PUT":
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


def process_ban_request(request, obj: Union[Type[BlogPost], Type[UserComment]], obj_id: int, ignore_or_ban):
    """
    Process a request that bans an object, or ignores its reports
    :param request: WSGI request
    :param obj: Object Model
    :param obj_id: ID of the object
    :param ignore_or_ban: True to ignore, False to ban
    """
    # if user is not authenticated or the method is not PUT
    # or the user is not staff member raise a Http404 error
    if not request.user.is_authenticated or not request.method == "PUT" or not request.user.is_staff:
        raise Http404()

    # if the database object does not exist raise Http404 error
    db_obj: BlogPost = obj.objects.get(id=obj_id)
    if not db_obj:
        raise Http404()

    if ignore_or_ban:
        db_obj.remove_reports()
        return JsonResponse({"success": "true", "status": "accepted"})
    else:
        db_obj.ban()
        return JsonResponse({"success": "true", "status": "banned"})


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


@method_decorator(csrf_exempt, name='dispatch')
def ban_post(request, post_id, *args, **kwargs):
    return process_ban_request(request, BlogPost, post_id, False)


@method_decorator(csrf_exempt, name='dispatch')
def ignore_reports_post(request, post_id, *args, **kwargs):
    return process_ban_request(request, BlogPost, post_id, True)


@method_decorator(csrf_exempt, name='dispatch')
def ban_comment(request, comment_id, *args, **kwargs):
    return process_ban_request(request, UserComment, comment_id, False)


@method_decorator(csrf_exempt, name='dispatch')
def ignore_reports_comment(request, comment_id, *args, **kwargs):
    return process_ban_request(request, UserComment, comment_id, True)


class ReportedPosts(ListView):
    queryset = BlogPost.objects.filter(reports__isnull=False, reports__reviewed=False).\
        prefetch_related('category', 'author')
    template_name = "interaction/reported_posts_list.html"

    def get_context_data(self, *args, **kwargs):
        # Restrict page only to staff users
        if not (self.request.user.is_authenticated or self.request.user.is_staff):
            raise Http404()
        return super().get_context_data(*args, **kwargs)


class ReportedComments(ListView):
    queryset = UserComment.objects.filter(reports__isnull=False, reports__reviewed=False)
    template_name = "interaction/reported_comments_list.html"

    def get_context_data(self, *args, **kwargs):
        # Restrict page only to staff users
        if not (self.request.user.is_authenticated or self.request.user.is_staff):
            raise Http404()
        return super().get_context_data(*args, **kwargs)