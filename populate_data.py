#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trilha_gamificada.settings')
django.setup()

from apps.workshops.models import Category, Workshop
from apps.gamification.models import Level, Badge

def create_sample_data():
    # Create Category
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
    
    # Create Levels
    levels_data = [
        {'name': 'Iniciante', 'min_xp': 0, 'color': '#6B7280', 'icon': 'fas fa-seedling'},
        {'name': 'Colaborador', 'min_xp': 300, 'color': '#3B82F6', 'icon': 'fas fa-lightbulb'},
        {'name': 'Inovador', 'min_xp': 800, 'color': '#8B5CF6', 'icon': 'fas fa-brain'},
        {'name': 'Líder', 'min_xp': 1500, 'color': '#F59E0B', 'icon': 'fas fa-crown'},
        {'name': 'Visionário', 'min_xp': 2500, 'color': '#EF4444', 'icon': 'fas fa-trophy'},
    ]
    
    for level_data in levels_data:
        Level.objects.get_or_create(
            name=level_data['name'],
            defaults=level_data
        )
    
    # Create Badges
    badges_data = [
        {
            'name': 'Primeiro Passo',
            'description': 'Complete seu primeiro workshop na trilha de inovação',
            'icon': 'fas fa-play',
            'color': '#10B981',
            'criteria_type': 'first_workshop',
            'criteria_value': 1
        },
        {
            'name': 'Canvas Master',
            'description': 'Complete o workshop de Business Model Canvas',
            'icon': 'fas fa-chart-pie',
            'color': '#FF6B35',
            'criteria_type': 'workshops_completed',
            'criteria_value': 1
        },
        {
            'name': 'Streak Fighter',
            'description': 'Mantenha uma sequência de 5 dias consecutivos',
            'icon': 'fas fa-fire',
            'color': '#F59E0B',
            'criteria_type': 'streak_days',
            'criteria_value': 5
        }
    ]
    
    for badge_data in badges_data:
        Badge.objects.get_or_create(
            name=badge_data['name'],
            defaults=badge_data
        )
    
    # Create Workshop
    workshop_data = {
        'title': 'Business Model Canvas',
        'slug': 'business-model-canvas',
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
            "Fontes de receita",
            "Estrutura de custos",
            "Recursos e parcerias chave",
            "Validação de hipóteses",
            "Cases práticos de startups"
        ],
        'is_active': True,
        'is_featured': True
    }
    
    Workshop.objects.get_or_create(
        slug='business-model-canvas',
        defaults=workshop_data
    )
    
    print("✅ Dados de exemplo criados com sucesso!")
    print("🎯 Workshop: Business Model Canvas")
    print("🏆 5 Níveis criados")
    print("🎖️ 3 Badges criados")
    print("📂 1 Categoria criada")

if __name__ == '__main__':
    create_sample_data()