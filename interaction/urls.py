from django.urls import path

from interaction import views

app_name = 'interaction'

urlpatterns = [
    path('like/post/<int:post_id>', views.like_post, name="like_post"),
    path('like/comment/<int:comment_id>', views.like_comment, name="like_comment"),

    path('report/post/<int:post_id>', views.report_post, name="report_post"),
    path('report/comment/<int:comment_id>', views.report_comment, name="report_comment"),

    path('report/post/remove/<int:post_id>', views.ignore_reports_post, name="accept_report_post"),
    path('report/post/ban/<int:post_id>', views.ban_post, name="ban_report_post"),
    path('report/comment/remove/<int:comment_id>', views.ignore_reports_comment, name="accept_report_comment"),
    path('report/comment/ban/<int:comment_id>', views.ban_comment, name="ban_report_comment"),

    path('reports/posts', views.ReportedPosts.as_view(), name="reported_posts"),
    path('reports/comments', views.ReportedComments.as_view(), name="reported_comments"),
]
