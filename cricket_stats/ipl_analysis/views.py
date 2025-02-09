from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Count, Q, F
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
import math

from .models import Season, StadiumInfo, Team, MatchInfo, PlayerTeamSeason, MatchTeam, Player
from .serializers import (
    SeasonSerializer,
    TeamSerializer,
    StadiumInfoSerializer,
    PlayerSerializer,
    MatchInfoSerializer,
)


# ============ Generic List and Detail Views ============

class SeasonListView(generics.ListAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer

class SeasonDetailView(generics.RetrieveAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer

class TeamListView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TeamDetailView(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class StadiumInfoListView(generics.ListAPIView):
    queryset = StadiumInfo.objects.all()
    serializer_class = StadiumInfoSerializer

class StadiumInfoDetailView(generics.RetrieveAPIView):
    queryset = StadiumInfo.objects.all()
    serializer_class = StadiumInfoSerializer

class PlayerListView(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerDetailView(generics.RetrieveAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class MatchInfoListView(generics.ListAPIView):
    queryset = MatchInfo.objects.all()
    serializer_class = MatchInfoSerializer

class MatchInfoDetailView(generics.RetrieveAPIView):
    queryset = MatchInfo.objects.all()
    serializer_class = MatchInfoSerializer


# ============ Custom API Views ============

class PlayerStatsView(APIView):
    """Retrieve a player's match and team statistics."""

    def get(self, request, player_name):
        player = get_object_or_404(Player, name=player_name)
        stats = player.get_matches_and_teams()
        return Response(stats)


class PlayersByTeamView(APIView):
    """Get all players who have played for a specific team."""

    def get(self, request, team_name):
        team = get_object_or_404(Team, team_name=team_name)

        player_associations = (
            PlayerTeamSeason.objects
            .filter(team=team)
            .select_related('player', 'season')
        )

        players = [
            {"player": assoc.player.name, "season": assoc.season.year}
            for assoc in player_associations
        ]

        return Response({"team": team_name, "players": players})
from django.db.models import Count, Q
from django.http import JsonResponse
from .models import Team, MatchInfo, MatchTeam

def team_stats(request, team_name):
    try:
        team = Team.objects.get(team_name=team_name)
        
        # Total matches played by the team
        total_matches = MatchTeam.objects.filter(team=team).count()
        
        # Home and away matches
        home_matches = MatchTeam.objects.filter(team=team, is_home_team=True).count()
        away_matches = MatchTeam.objects.filter(team=team, is_home_team=False).count()
        
        # Get matches where this team participated
        team_matches = MatchInfo.objects.filter(teams__team=team)
        
        # Total wins - only count matches where this team was the winner
        wins = team_matches.filter(match_winner=team).count()
        
        # Total losses - count matches where team participated but wasn't the winner
        losses = team_matches.exclude(match_winner=team).count()
        
        # Win percentage
        win_perc = (wins / total_matches) * 100 if total_matches > 0 else 0
        
        # Opponent-wise performance
        opponents = Team.objects.exclude(id=team.id)
        performance = []
        
        for opp in opponents:
            # Get matches between these two teams
            matches_with_opp = MatchInfo.objects.filter(
                teams__team=team
            ).filter(
                teams__team=opp
            )
            
            # Wins against this opponent
            wins_against_opp = matches_with_opp.filter(
                match_winner=team
            ).count()
            
            # Total matches against this opponent
            total_matches_against_opp = matches_with_opp.count()
            
            # Losses against this opponent
            losses_against_opp = total_matches_against_opp - wins_against_opp
            
            # Calculate win percentage
            win_percentage_against_opp =math.floor (
                (wins_against_opp / total_matches_against_opp) * 100 
                if total_matches_against_opp > 0 
                else 0
            )
            
            if total_matches_against_opp > 0:  # Only include opponents they've played against
                performance.append({
                    "opponent": opp.team_name,
                    "wins": wins_against_opp,
                    "losses": losses_against_opp,
                    "total_matches": total_matches_against_opp,
                    "win_percentage": round(win_percentage_against_opp, 2)
                })
        
        # Final response
        stats = {
            "team_name": team_name,
            "total_matches": total_matches,
            "home_matches": home_matches,
            "away_matches": away_matches,
            "wins": wins,
            "losses": losses,
            "win_percentage": round(win_perc, 2),
            "opponent_performance": performance
        }
        
        return JsonResponse(stats)
    
    except Team.DoesNotExist:
        return JsonResponse({"error": f"Team '{team_name}' not found"}, status=404)

