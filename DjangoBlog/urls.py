import debug_toolbar
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from DjangoBlog import settings
from blog import urls as blog_urls
from account import urls as account_urls
from category import urls as category_urls
from interaction import urls as interaction_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(blog_urls)),
    path('account/', include(account_urls)),
    path('category/', include(category_urls)),
    path('action/', include(interaction_urls)),
    path('__debug__/', include(debug_toolbar.urls)),
]

# Add static and media files to site URLs
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
               + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
