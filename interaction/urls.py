from django.urls import path

from interaction import views

app_name = 'interaction'

urlpatterns = [
    path('like/post/<int:post_id>', views.like_post, name="like_post"),
    path('like/comment/<int:comment_id>', views.like_comment, name="like_comment"),
]
