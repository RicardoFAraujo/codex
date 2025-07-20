from django.urls import path
from . import views

app_name = 'gamification'

urlpatterns = [
    path('badges/', views.BadgeListView.as_view(), name='badges'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    path('challenges/', views.ChallengeListView.as_view(), name='challenges'),
]