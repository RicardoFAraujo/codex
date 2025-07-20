from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Level(models.Model):
    """User levels based on XP"""
    name = models.CharField('Nome', max_length=50)
    min_xp = models.PositiveIntegerField('XP Mínimo')
    color_gradient = models.CharField('Gradiente de Cor', max_length=100, default='from-gray-400 to-gray-600')
    icon = models.CharField('Ícone', max_length=50, default='fas fa-user')
    description = models.TextField('Descrição', blank=True)
    
    class Meta:
        verbose_name = 'Nível'
        verbose_name_plural = 'Níveis'
        ordering = ['min_xp']
    
    def __str__(self):
        return f'{self.name} ({self.min_xp} XP)'


class Badge(models.Model):
    """Achievement badges"""
    CRITERIA_CHOICES = [
        ('workshops_completed', 'Workshops Concluídos'),
        ('streak_days', 'Dias Consecutivos'),
        ('total_xp', 'XP Total'),
        ('first_workshop', 'Primeiro Workshop'),
        ('level_reached', 'Nível Alcançado'),
        ('custom', 'Critério Personalizado'),
    ]
    
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição')
    icon = models.CharField('Ícone', max_length=50, default='fas fa-award')
    color_gradient = models.CharField('Gradiente de Cor', max_length=100, default='from-blue-400 to-blue-600')
    
    # Criteria
    criteria_type = models.CharField('Tipo de Critério', max_length=20, choices=CRITERIA_CHOICES)
    criteria_value = models.PositiveIntegerField('Valor do Critério', help_text='Valor necessário para conquistar o badge')
    
    # Status
    is_active = models.BooleanField('Ativo', default=True)
    is_rare = models.BooleanField('Raro', default=False)
    
    # Order and visibility
    order = models.PositiveIntegerField('Ordem', default=0)
    
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Badge'
        verbose_name_plural = 'Badges'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def check_criteria(self, user):
        """Check if user meets criteria for this badge"""
        if self.criteria_type == 'workshops_completed':
            return user.completed_workshops.count() >= self.criteria_value
        elif self.criteria_type == 'streak_days':
            return user.get_current_streak() >= self.criteria_value
        elif self.criteria_type == 'total_xp':
            return user.total_xp >= self.criteria_value
        elif self.criteria_type == 'first_workshop':
            return user.completed_workshops.count() >= 1
        elif self.criteria_type == 'level_reached':
            current_level = user.get_current_level()
            return current_level and current_level.min_xp >= self.criteria_value
        
        return False


class UserBadge(models.Model):
    """User earned badges"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='earned_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField('Conquistado em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Badge do Usuário'
        verbose_name_plural = 'Badges dos Usuários'
        unique_together = ['user', 'badge']
        ordering = ['-earned_at']
    
    def __str__(self):
        return f'{self.user} - {self.badge.name}'


class Challenge(models.Model):
    """Temporary challenges for users"""
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição')
    
    # Requirements
    target_value = models.PositiveIntegerField('Valor Alvo')
    challenge_type = models.CharField('Tipo', max_length=50, choices=[
        ('workshops_week', 'Workshops na Semana'),
        ('streak_challenge', 'Desafio de Sequência'),
        ('xp_challenge', 'Desafio de XP'),
    ])
    
    # Rewards
    xp_reward = models.PositiveIntegerField('Recompensa XP', default=100)
    badge_reward = models.ForeignKey(Badge, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Badge de Recompensa')
    
    # Timeline
    start_date = models.DateTimeField('Data de Início')
    end_date = models.DateTimeField('Data de Fim')
    
    # Status
    is_active = models.BooleanField('Ativo', default=True)
    
    class Meta:
        verbose_name = 'Desafio'
        verbose_name_plural = 'Desafios'
        ordering = ['-start_date']
    
    def __str__(self):
        return self.name


class UserChallenge(models.Model):
    """User challenge progress"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    current_progress = models.PositiveIntegerField('Progresso Atual', default=0)
    is_completed = models.BooleanField('Concluído', default=False)
    completed_at = models.DateTimeField('Concluído em', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Desafio do Usuário'
        verbose_name_plural = 'Desafios dos Usuários'
        unique_together = ['user', 'challenge']
    
    def __str__(self):
        return f'{self.user} - {self.challenge.name}'
    
    @property
    def progress_percentage(self):
        """Calculate progress percentage"""
        if self.challenge.target_value == 0:
            return 100
        return min(100, (self.current_progress / self.challenge.target_value) * 100)