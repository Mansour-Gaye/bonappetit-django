from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Add any model specific admin configurations here
    # For example, if you added fields to CustomUser that you want to display in the admin
    # list_display = UserAdmin.list_display + ('phone', 'is_client', 'is_gestionnaire')
    # fieldsets = UserAdmin.fieldsets + (
    #     (None, {'fields': ('phone', 'is_client', 'is_gestionnaire')}),
    # )
    # add_fieldsets = UserAdmin.add_fieldsets + (
    #     (None, {'fields': ('phone', 'is_client', 'is_gestionnaire')}),
    # )
    pass

admin.site.register(CustomUser, CustomUserAdmin)
