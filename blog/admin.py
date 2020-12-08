from django.contrib import admin
from blog.models import BlogPost, UserComment, UserModel
from django.contrib.auth.admin import UserAdmin


class UserAdminExt(UserAdmin):
    list_display = ('email', 'username', 'user_type')
    search_fields = ('email', 'username')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(UserModel, UserAdminExt)
admin.site.register(BlogPost)
admin.site.register(UserComment)
