from django.urls import path

from category import views as category_views

app_name = 'category'

urlpatterns = [
    path('<int:pk>', category_views.CategoryPostsView.as_view(), name="category"),
    path('', category_views.CategoryView.as_view(), name="categories"),
]
