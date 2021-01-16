from django.contrib import admin

from blog.models import BlogPost, UserComment

admin.site.register(BlogPost)
admin.site.register(UserComment)
