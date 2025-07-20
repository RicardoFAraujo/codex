from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.workshops.models import Workshop
from apps.gamification.models import Badge, Level


class HomeView(TemplateView):
    """Landing page view for non-authenticated users"""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workshops'] = Workshop.objects.filter(is_active=True)[:6]
        context['badges'] = Badge.objects.filter(is_active=True)[:8]
        context['levels'] = Level.objects.all().order_by('min_xp')
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard view for authenticated users"""
    template_name = 'core/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # User progress data
        context['user_progress'] = {
            'level': user.get_current_level(),
            'current_xp': user.total_xp,
            'next_level_xp': user.get_next_level_xp(),
            'completed_workshops': user.completed_workshops.count(),
            'earned_badges': user.earned_badges.count(),
            'streak': user.get_current_streak(),
        }
        
        # Available workshops
        context['available_workshops'] = Workshop.objects.filter(
            is_active=True
        ).exclude(
            participants=user
        )
        
        # Recent achievements
        context['recent_badges'] = user.earned_badges.all()[:3]
        
        return context