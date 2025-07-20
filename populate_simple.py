#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trilha_gamificada.settings')
django.setup()

from apps.workshops.models import Category, Workshop
from apps.gamification.models import Level, Badge
from django.utils import timezone

def create_sample_data():
    print("🚀 Iniciando criação de dados de exemplo...")
    
    # 1. Create Category
    print("\n📂 Criando categoria...")
    category, created = Category.objects.get_or_create(
        slug='empreendedorismo-negocios',
        defaults={
            'name': 'Empreendedorismo e Negócios',
            'description': 'Workshops focados em desenvolvimento de negócios, empreendedorismo e estratégias empresariais',
            'color': '#FF6B35',
            'icon': 'fas fa-chart-line',
            'is_active': True
        }
    )
    print(f"✅ Categoria: {category.name} {'(criada)' if created else '(já existe)'}")
    
    # 2. Create Levels
    print("\n🏆 Criando níveis...")
    levels_data = [
        {'name': 'Iniciante', 'min_xp': 0, 'color': '#6B7280', 'icon': 'fas fa-seedling', 'description': 'Bem-vindo à jornada!'},
        {'name': 'Colaborador', 'min_xp': 300, 'color': '#3B82F6', 'icon': 'fas fa-lightbulb', 'description': 'Você está progredindo!'},
        {'name': 'Inovador', 'min_xp': 800, 'color': '#8B5CF6', 'icon': 'fas fa-brain', 'description': 'Excelente progresso!'},
        {'name': 'Líder', 'min_xp': 1500, 'color': '#F59E0B', 'icon': 'fas fa-crown', 'description': 'Você é um líder!'},
        {'name': 'Visionário', 'min_xp': 2500, 'color': '#EF4444', 'icon': 'fas fa-trophy', 'description': 'Nível máximo!'},
    ]
    
    for level_data in levels_data:
        level, created = Level.objects.get_or_create(
            name=level_data['name'],
            defaults=level_data
        )
        print(f"✅ Nível: {level.name} ({level.min_xp} XP) {'(criado)' if created else '(já existe)'}")
    
    # 3. Create Badges
    print("\n🎖️ Criando badges...")
    badges_data = [
        {'name': 'Primeiro Passo', 'description': 'Complete seu primeiro workshop', 'icon': 'fas fa-play', 'color': '#10B981', 'criteria_type': 'first_workshop', 'criteria_value': 1},
        {'name': 'Canvas Master', 'description': 'Complete o workshop de Canvas', 'icon': 'fas fa-chart-pie', 'color': '#FF6B35', 'criteria_type': 'workshops_completed', 'criteria_value': 1},
        {'name': 'Streak Fighter', 'description': 'Mantenha 5 dias consecutivos', 'icon': 'fas fa-fire', 'color': '#F59E0B', 'criteria_type': 'streak_days', 'criteria_value': 5},
    ]
    
    for badge_data in badges_data:
        badge, created = Badge.objects.get_or_create(
            name=badge_data['name'],
            defaults=badge_data
        )
        print(f"✅ Badge: {badge.name} {'(criado)' if created else '(já existe)'}")
    
    # 4. Create Workshop
    print("\n🎯 Criando workshop...")
    
    # Datas para o workshop (próxima semana)
    start_date = timezone.now() + timedelta(days=7)
    end_date = start_date + timedelta(hours=6)
    registration_deadline = start_date - timedelta(days=2)
    
    workshop_data = {
        'title': 'Business Model Canvas',
        'subtitle': 'Construa modelos de negócio inovadores',
        'description': 'Aprenda a usar a ferramenta Business Model Canvas para desenvolver, visualizar e testar modelos de negócio de forma estruturada e colaborativa.',
        'category': category,
        'duration': '6h',
        'format': 'workshop',
        'level': 'intermediario',
        'max_participants': 20,
        'instructor': 'Prof. Ana Startup',
        'instructor_bio': 'Empreendedora serial com mais de 10 anos de experiência em startups.',
        'xp_reward': 200,
        'highlights': [
            "9 blocos do Business Model Canvas",
            "Proposta de valor única",
            "Segmentação de clientes",
            "Canais de distribuição",
            "Fontes de receita"
        ],
        'start_date': start_date,
        'end_date': end_date,
        'registration_deadline': registration_deadline,
        'is_active': True,
        'is_featured': True
    }
    
    workshop, created = Workshop.objects.get_or_create(
        slug='business-model-canvas',
        defaults=workshop_data
    )
    print(f"✅ Workshop: {workshop.title} {'(criado)' if created else '(já existe)'}")
    
    print("\n🎉 DADOS CRIADOS COM SUCESSO!")
    print("=" * 50)
    print("📊 RESUMO:")
    print(f"📂 Categorias: {Category.objects.count()}")
    print(f"🎯 Workshops: {Workshop.objects.count()}")
    print(f"🏆 Níveis: {Level.objects.count()}")
    print(f"🎖️ Badges: {Badge.objects.count()}")
    print("=" * 50)
    print("🔗 Acesse o admin: http://127.0.0.1:8000/admin/")
    print("🌐 Inicie o servidor: python manage.py runserver")

if __name__ == '__main__':
    create_sample_data()
