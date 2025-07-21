from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUsers

class CustomUserAdmin(UserAdmin):
    model = AppUsers
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'phone', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'first_name',
                                                 'last_name', 'password1', 'password2',
                                                 'phone', 'date_of_birth'), }),
    )

    ordering = ('email',)
    list_filter = ('is_active', 'is_staff', 'date_joined')

admin.site.register(AppUsers, CustomUserAdmin)

