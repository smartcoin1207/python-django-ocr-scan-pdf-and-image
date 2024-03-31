"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import TokenProxy


from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['name', 'email', 'company']
    fieldsets = (
        (None, {'fields': ('email', 'name', 'code', 'password', 'company', 'role')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Secret for resetting password'), {'fields': ('reset_password_secret',)}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['reset_password_secret','last_login']
    add_fieldsets = [
        [None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'code',
                'company',
                'role',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }]
    ]

class CompanyAdmin(admin.ModelAdmin):
    ordering = ['created_at']
    list_display = ['name', 'address', 'phone']
    readonly_fields = ('id',)

class ClientAdmin(admin.ModelAdmin):
    ordering = ['created_at']
    list_display = ['name', 'address', 'phone']
    readonly_fields = ('id',)

admin.site.unregister(TokenProxy)
admin.site.unregister(Group)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Company, CompanyAdmin)
admin.site.register(models.Client, ClientAdmin)
