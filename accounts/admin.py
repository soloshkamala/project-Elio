from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser


    list_display = ['username', 'email', 'role', 'is_psychologist_verified', 'is_active']

    list_filter = ['role', 'is_psychologist_verified', 'is_active']

    fieldsets = UserAdmin.fieldsets + (
        ('Дані ELIO (Для психологів та ролей)', {
            'fields': ('role', 'is_psychologist_verified', 'bio', 'diploma_file')
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)