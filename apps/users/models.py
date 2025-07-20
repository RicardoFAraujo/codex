from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    """Custom User model with gamification features"""
    
    # Personal info
    full_name = models.CharField('Nome completo', max_length=255, blank=True)
    department = models.CharField('Departamento', max_length=100, blank=True)
    position = models.CharField('Cargo', max_length=100, blank=True)
    
    # Gamification fields
    total_xp = models.PositiveIntegerField('XP Total', default=0)
    current_streak = models.PositiveIntegerField('Sequência atual', default=0)
    longest_streak = models.PositiveIntegerField('Maior sequência', default=0)
    last_activity_date = models.DateField('Última atividade', null=True, blank=True)
    
    # Profile
    avatar = models.ImageField('Avatar', upload_to='avatars/', blank=True, null=True)
    bio = models.TextField('Biografia', blank=True, max_length=500)
    
    # Timestamps
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-total_xp', 'username']
    
    def __str__(self):
        return self.get_full_name() or self.username
    
    def get_full_name(self):
        return self.full_name or f"{self.first_name} {self.last_name}".strip()
    
    def get_current_level(self):
        """Get user's current level based on XP"""
        from apps.gamification.models import Level
        return Level.objects.filter(min_xp__lte=self.total_xp).order_by('-min_xp').first()
    
    def get_next_level(self):
        """Get user's next level"""
        from apps.gamification.models import Level
        return Level.objects.filter(min_xp__gt=self.total_xp).order_by('min_xp').first()
    
    def get_next_level_xp(self):
        """Get XP needed for next level"""
        next_level = self.get_next_level()
        return next_level.min_xp if next_level else self.total_xp
    
    def add_xp(self, amount):
        """Add XP to user and update activity"""
        self.total_xp += amount
        self.update_streak()
        self.save()
        
        # Check for new badges
        self.check_and_award_badges()
    
    def update_streak(self):
        """Update user's activity streak"""
        today = timezone.now().date()
        
        if self.last_activity_date:
            days_diff = (today - self.last_activity_date).days
            
            if days_diff == 1:
                # Consecutive day
                self.current_streak += 1
            elif days_diff > 1:
                # Streak broken
                self.current_streak = 1
            # If days_diff == 0, same day, don't change streak
        else:
            # First activity
            self.current_streak = 1
        
        # Update longest streak
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
        
        self.last_activity_date = today
    
    def get_current_streak(self):
        """Get current streak, checking if it's still valid"""
        if not self.last_activity_date:
            return 0
        
        today = timezone.now().date()
        days_diff = (today - self.last_activity_date).days
        
        if days_diff <= 1:
            return self.current_streak
        else:
            # Streak is broken, reset it
            self.current_streak = 0
            self.save()
            return 0
    
    def check_and_award_badges(self):
        """Check and award badges based on user progress"""
        from apps.gamification.models import Badge, UserBadge
        
        # Get all badges user doesn't have yet
        earned_badge_ids = self.earned_badges.values_list('badge_id', flat=True)
        available_badges = Badge.objects.filter(is_active=True).exclude(id__in=earned_badge_ids)
        
        for badge in available_badges:
            if badge.check_criteria(self):
                UserBadge.objects.create(user=self, badge=badge)
    
    def get_ranking_position(self):
        """Get user's position in global ranking"""
        return User.objects.filter(total_xp__gt=self.total_xp).count() + 1


