from django.contrib import admin

# Register your models here.

from user.models import UserProfile


class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'mobile', 'email', 'avatar', 'is_staff']
    search_fields = ['id', 'username']
    list_display = ['id', 'username', 'mobile', 'email', 'is_staff', 'create_at', 'update_at']



admin.site.register(UserProfile, UserAdmin)
