from django.contrib import admin

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from user.forms import AccountAdminCreationForm, AccountAdminChangeForm
from . import models


    

class AccountAdmin(BaseUserAdmin):

    form = AccountAdminChangeForm
    add_form = AccountAdminCreationForm

    list_display = ('email', 'status', 'is_staff', 'is_superuser', 'user_type') 
    list_filter = ('status', 'is_staff', 'is_superuser')
    fieldsets = (
        ('Account', {'fields': ('email', 'password')}),
        ('Account Status', {'fields': ('status', 'user_type')}),
        ('Permissions', {'fields': ('is_active','is_staff','is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'status',  'is_staff', 'is_superuser', 'user_type')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    # inlines = (UserProfileInline,)


admin.site.register(models.Account, AccountAdmin)
