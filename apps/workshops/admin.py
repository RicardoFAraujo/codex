from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Level, Workshop, Enrollment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_display', 'icon_display', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    
    def color_display(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 50%; display: inline-block;"></div>',
            obj.color
        )
    color_display.short_description = 'Cor'
    
    def icon_display(self, obj):
        return format_html('<i class="{}"></i>', obj.icon)
    icon_display.short_description = 'Ícone'


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_display', 'order')
    ordering = ('order',)
    
    def color_display(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 50%; display: inline-block;"></div>',
            obj.color
        )
    color_display.short_description = 'Cor'


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    readonly_fields = ('enrolled_at', 'completed_at')


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'level', 'format', 'xp_reward', 'enrolled_count', 'is_active', 'start_date')
    list_filter = ('category', 'level', 'format', 'is_active', 'is_featured', 'created_at')
    search_fields = ('title', 'description', 'instructor_name')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('participants',)
    inlines = [EnrollmentInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('title', 'slug', 'subtitle', 'description')
        }),
        ('Classificação', {
            'fields': ('category', 'level', 'format')
        }),
        ('Detalhes do Workshop', {
            'fields': ('duration', 'max_participants', 'highlights', 'xp_reward')
        }),
        ('Instrutor', {
            'fields': ('instructor_name', 'instructor_bio', 'instructor_avatar')
        }),
        ('Agendamento', {
            'fields': ('start_date', 'end_date', 'registration_deadline')
        }),
        ('Mídia', {
            'fields': ('image', 'gradient_colors')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
    )
    
    def enrolled_count(self, obj):
        return obj.enrollments.filter(status='enrolled').count()
    enrolled_count.short_description = 'Inscritos'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'workshop', 'status', 'enrolled_at', 'rating')
    list_filter = ('status', 'workshop__category', 'enrolled_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'workshop__title')
    readonly_fields = ('enrolled_at',)
    
    actions = ['mark_completed', 'mark_cancelled']
    
    def mark_completed(self, request, queryset):
        for enrollment in queryset:
            enrollment.complete()
        self.message_user(request, f'{queryset.count()} inscrições marcadas como concluídas.')
    mark_completed.short_description = 'Marcar como concluído'
    
    def mark_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f'{queryset.count()} inscrições canceladas.')
    mark_cancelled.short_description = 'Cancelar inscrições'