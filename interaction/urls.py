from django.urls import path

from interaction import views

app_name = 'interaction'

urlpatterns = [
    path('/like/post/<int:post_id>', views.like_post, name="like_post"),
    # path('like/comment/<int:id>', category_views.CategoryPostsView.as_view(), name="like_comment"),
]
