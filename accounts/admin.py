from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTPVerification

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_psychologist_verified', 'is_premium', 'is_banned')
    list_filter = ('role', 'is_psychologist_verified', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = (
        ('Авторизація', {'fields': ('username', 'password')}),
        ('Контакти та Профіль', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'birth_date', 'gender', 'avatar')
        }),
        ('Ментальний стан (Клієнт)', {
            'fields': ('core_issues',)
        }),
        ('Спеціаліст (Психолог)', {
            'fields': ('bio', 'diploma_file', 'is_psychologist_verified')
        }),
        ('Системні ролі та Доступи', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Монетизація та Санкції', {
            'fields': ('premium_until', 'banned_until', 'reminders_enabled')
        }),
        ('Важливі дати', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTPVerification)