from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import UserModel


class UserAdminExt(UserAdmin):
    list_display = ('email', 'username', 'user_type')
    search_fields = ('email', 'username')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(UserModel, UserAdminExt)
