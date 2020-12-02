import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from blog import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urls)),
    path('__debug__/', include(debug_toolbar.urls)),
]
