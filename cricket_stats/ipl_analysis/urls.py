from django.urls import path
from .views import (
    SeasonListView, SeasonDetailView,
    TeamListView, TeamDetailView,
    StadiumInfoListView, StadiumInfoDetailView,
    PlayerListView, PlayerDetailView,
    MatchInfoListView, MatchInfoDetailView,
    PlayerStatsView, PlayersByTeamView, team_stats
)

urlpatterns = [
    # Season URLs
    path('seasons/', SeasonListView.as_view(), name='season-list'),
    path('seasons/<int:pk>/', SeasonDetailView.as_view(), name='season-detail'),

    # Team URLs
    path('teams/', TeamListView.as_view(), name='team-list'),
    path('teams/<int:pk>/', TeamDetailView.as_view(), name='team-detail'),

    # Stadium Info URLs
    path('stadiums/', StadiumInfoListView.as_view(), name='stadium-list'),
    path('stadiums/<int:pk>/', StadiumInfoDetailView.as_view(), name='stadium-detail'),

    # Player URLs
    path('players/', PlayerListView.as_view(), name='player-list'),
    path('players/<int:pk>/', PlayerDetailView.as_view(), name='player-detail'),

    # Match Info URLs
    path('matches/', MatchInfoListView.as_view(), name='match-list'),
    path('matches/<int:pk>/', MatchInfoDetailView.as_view(), name='match-detail'),

    # Custom API Endpoints
    path('player-stats/<str:player_name>/', PlayerStatsView.as_view(), name='player-stats'),
    path('team-players/<str:team_name>/', PlayersByTeamView.as_view(), name='team-players'),
    path('team-stats/<str:team_name>/', team_stats, name='team-stats'),
]
