from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'balance_sats', 'is_admin_user', 'is_active', 'date_joined')
    list_filter = ('is_admin_user', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('BitSport', {'fields': ('balance_sats', 'is_admin_user')}),
    )
    search_fields = ('username', 'email')
