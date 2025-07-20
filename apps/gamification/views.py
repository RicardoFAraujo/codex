from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .models import Badge, UserBadge, Challenge, UserChallenge

User = get_user_model()


class BadgeListView(ListView):
    """List all available badges"""
    model = Badge
    template_name = 'gamification/badges.html'
    context_object_name = 'badges'
    
    def get_queryset(self):
        return Badge.objects.filter(is_active=True).order_by('order', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            # Get user's earned badges
            earned_badge_ids = UserBadge.objects.filter(
                user=self.request.user
            ).values_list('badge_id', flat=True)
            
            context['earned_badge_ids'] = list(earned_badge_ids)
        else:
            context['earned_badge_ids'] = []
            
        return context


class LeaderboardView(ListView):
    """Global leaderboard"""
    model = User
    template_name = 'gamification/leaderboard.html'
    context_object_name = 'users'
    paginate_by = 50
    
    def get_queryset(self):
        return User.objects.filter(
            is_active=True,
            total_xp__gt=0
        ).order_by('-total_xp')[:50]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            context['user_position'] = self.request.user.get_ranking_position()
        
        return context


class ChallengeListView(LoginRequiredMixin, ListView):
    """List active challenges"""
    model = Challenge
    template_name = 'gamification/challenges.html'
    context_object_name = 'challenges'
    
    def get_queryset(self):
        from django.utils import timezone
        return Challenge.objects.filter(
            is_active=True,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get user's challenge progress
        user_challenges = UserChallenge.objects.filter(
            user=self.request.user,
            challenge__in=context['challenges']
        ).select_related('challenge')
        
        # Create a dictionary for easy lookup
        challenge_progress = {
            uc.challenge_id: uc for uc in user_challenges
        }
        
        context['challenge_progress'] = challenge_progress
        
        return context