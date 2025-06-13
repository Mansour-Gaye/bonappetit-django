from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'is_client', 'is_gestionnaire')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone', 'is_client', 'is_gestionnaire')}),
    )
    list_display = UserAdmin.list_display + ('is_client', 'is_gestionnaire')

admin.site.register(CustomUser, CustomUserAdmin)
