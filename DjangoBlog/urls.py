import debug_toolbar
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from DjangoBlog import settings
from blog import urls

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include(urls)),
                  path('__debug__/', include(debug_toolbar.urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
