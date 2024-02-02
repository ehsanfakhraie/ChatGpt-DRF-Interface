from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    readonly_fields = ['license_code']
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('license_code', 'tokens')}),
    )


admin.site.register(User, CustomUserAdmin)
