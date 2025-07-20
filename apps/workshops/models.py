from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from PIL import Image

User = get_user_model()


class Category(models.Model):
    """Categories for workshops"""
    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Slug', unique=True)
    description = models.TextField('Descrição', blank=True)
    color = models.CharField('Cor', max_length=7, default='#0072CE', help_text='Cor em hexadecimal')
    icon = models.CharField('Ícone', max_length=50, default='fas fa-lightbulb', help_text='Classe do ícone FontAwesome')
    is_active = models.BooleanField('Ativo', default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return self.name


class Level(models.Model):
    """Difficulty levels for workshops"""
    LEVEL_CHOICES = [
        ('iniciante', 'Iniciante'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
    ]
    
    name = models.CharField('Nome', max_length=20, choices=LEVEL_CHOICES, unique=True)
    color = models.CharField('Cor', max_length=7, default='#28a745')
    order = models.PositiveIntegerField('Ordem', default=0)

    class Meta:
        verbose_name = 'Nível de Dificuldade'
        verbose_name_plural = 'Níveis de Dificuldade'
        ordering = ['order']

    def __str__(self):
        return self.get_name_display()


class Workshop(models.Model):
    """Workshop model"""
    FORMAT_CHOICES = [
        ('workshop', 'Workshop'),
        ('minicurso', 'Minicurso'),
        ('palestra', 'Palestra'),
        ('hands_on', 'Hands-on'),
    ]

    # Basic info
    title = models.CharField('Título', max_length=200)
    slug = models.SlugField('Slug', unique=True)
    subtitle = models.CharField('Subtítulo', max_length=300, blank=True)
    description = models.TextField('Descrição')
    
    # Classification
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoria')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, verbose_name='Nível')
    format = models.CharField('Formato', max_length=20, choices=FORMAT_CHOICES, default='workshop')
    
    # Content
    duration = models.CharField('Duração', max_length=50, help_text='Ex: 4h, 2 dias')
    max_participants = models.PositiveIntegerField('Máximo de Participantes', default=30)
    highlights = models.JSONField('Destaques', default=list, help_text='Lista de tópicos principais')
    
    # Instructor
    instructor_name = models.CharField('Nome do Instrutor', max_length=200)
    instructor_bio = models.TextField('Bio do Instrutor', blank=True)
    instructor_avatar = models.ImageField('Avatar do Instrutor', upload_to='instructors/', blank=True)
    
    # Gamification
    xp_reward = models.PositiveIntegerField('Recompensa XP', default=100)
    
    # Scheduling
    start_date = models.DateTimeField('Data de Início', null=True, blank=True)
    end_date = models.DateTimeField('Data de Fim', null=True, blank=True)
    registration_deadline = models.DateTimeField('Prazo de Inscrição', null=True, blank=True)
    
    # Media
    image = models.ImageField('Imagem', upload_to='workshops/', blank=True)
    gradient_colors = models.CharField(
        'Cores do Gradiente', 
        max_length=100, 
        default='from-blue-500 to-purple-500',
        help_text='Classes Tailwind para gradiente'
    )
    
    # Status
    is_active = models.BooleanField('Ativo', default=True)
    is_featured = models.BooleanField('Destaque', default=False)
    
    # Participants
    participants = models.ManyToManyField(
        User, 
        through='Enrollment', 
        related_name='enrolled_workshops',
        blank=True
    )
    
    # Timestamps
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Workshop'
        verbose_name_plural = 'Workshops'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('workshops:detail', kwargs={'slug': self.slug})

    @property
    def is_registration_open(self):
        """Check if registration is still open"""
        if not self.registration_deadline:
            return True
        return timezone.now() < self.registration_deadline

    @property
    def available_spots(self):
        """Get number of available spots"""
        enrolled_count = self.enrollments.filter(status='enrolled').count()
        return max(0, self.max_participants - enrolled_count)

    @property
    def is_full(self):
        """Check if workshop is full"""
        return self.available_spots == 0

    def save(self, *args, **kwargs):
        # Resize image if needed
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 400 or img.width > 600:
                output_size = (600, 400)
                img.thumbnail(output_size)
                img.save(self.image.path)


class Enrollment(models.Model):
    """Enrollment model for workshop participants"""
    STATUS_CHOICES = [
        ('enrolled', 'Inscrito'),
        ('completed', 'Concluído'),
        ('cancelled', 'Cancelado'),
        ('no_show', 'Faltou'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, verbose_name='Workshop', related_name='enrollments')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='enrolled')
    enrolled_at = models.DateTimeField('Inscrito em', auto_now_add=True)
    completed_at = models.DateTimeField('Concluído em', null=True, blank=True)
    feedback = models.TextField('Feedback', blank=True)
    rating = models.PositiveIntegerField('Avaliação', null=True, blank=True, choices=[(i, i) for i in range(1, 6)])

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = ['user', 'workshop']
        ordering = ['-enrolled_at']

    def __str__(self):
        return f'{self.user} - {self.workshop.title}'

    def complete(self):
        """Mark enrollment as completed and award XP"""
        if self.status != 'completed':
            self.status = 'completed'
            self.completed_at = timezone.now()
            self.save()
            
            # Award XP to user
            self.user.add_xp(self.workshop.xp_reward)
            
            # Add to completed workshops (many-to-many relation)
            if hasattr(self.user, 'completed_workshops'):
                self.user.completed_workshops.add(self.workshop)