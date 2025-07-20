from django.contrib import admin
from django.utils.html import format_html
from .models import Level, Badge, UserBadge, Challenge, UserChallenge


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'min_xp', 'color_display', 'icon_display')
    ordering = ('min_xp',)
    
    def color_display(self, obj):
        return format_html(
            '<div class="bg-gradient-to-r {} w-20 h-6 rounded"></div>',
            obj.color_gradient
        )
    color_display.short_description = 'Cor'
    
    def icon_display(self, obj):
        return format_html('<i class="{}"></i>', obj.icon)
    icon_display.short_description = 'Ícone'


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'criteria_type', 'criteria_value', 'color_display', 'is_active', 'is_rare')
    list_filter = ('criteria_type', 'is_active', 'is_rare')
    search_fields = ('name', 'description')
    ordering = ('order', 'name')
    
    def color_display(self, obj):
        return format_html(
            '<div class="bg-gradient-to-r {} w-20 h-6 rounded"></div>',
            obj.color_gradient
        )
    color_display.short_description = 'Cor'


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'earned_at')
    list_filter = ('badge', 'earned_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'badge__name')
    readonly_fields = ('earned_at',)


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('name', 'challenge_type', 'target_value', 'xp_reward', 'start_date', 'end_date', 'is_active')
    list_filter = ('challenge_type', 'is_active', 'start_date')
    search_fields = ('name', 'description')


@admin.register(UserChallenge)
class UserChallengeAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'current_progress', 'progress_percentage', 'is_completed')
    list_filter = ('challenge', 'is_completed')
    search_fields = ('user__username', 'challenge__name')
    readonly_fields = ('completed_at',)