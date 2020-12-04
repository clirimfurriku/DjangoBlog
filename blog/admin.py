from django.contrib import admin
from blog.models import BlogPost, UserComment, UserModel

admin.site.register(BlogPost)
admin.site.register(UserModel)
admin.site.register(UserComment)
