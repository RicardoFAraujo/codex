from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'get_full_name', 'email', 'department', 'total_xp', 'current_level_display', 'current_streak', 'is_active')
    list_filter = ('is_active', 'is_staff', 'department', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'full_name')
    ordering = ('-total_xp',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informações Pessoais', {
            'fields': ('full_name', 'department', 'position', 'avatar', 'bio')
        }),
        ('Gamificação', {
            'fields': ('total_xp', 'current_streak', 'longest_streak', 'last_activity_date')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': ('full_name', 'department', 'position')
        }),
    )
    
    def current_level_display(self, obj):
        level = obj.get_current_level()
        if level:
            return format_html(
                '<span style="background: linear-gradient(45deg, #0072CE, #F9423A); color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
                level.name
            )
        return '-'
    current_level_display.short_description = 'Nível Atual'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()