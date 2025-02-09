
# Create your models here.
from django.db import models

class Season(models.Model):
    year = models.CharField(max_length=10, unique=True, verbose_name="Season Year")
    
    def __str__(self):
        return f"Season {self.year}"

class Team(models.Model):
    team_name = models.CharField(max_length=255, unique=True, verbose_name="Team Name")
    
    def __str__(self):
        return self.team_name

class StadiumInfo(models.Model):
    stadium_name = models.CharField(max_length=255, verbose_name="Stadium Name")
    city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.stadium_name} in {self.city}"



class MatchInfo(models.Model):
    
    match_city = models.ForeignKey(StadiumInfo, on_delete=models.CASCADE, verbose_name="Match City", 
                                  related_name="match_city", null=True, blank=True)
    match_stadium = models.ForeignKey(StadiumInfo, on_delete=models.CASCADE, verbose_name="Match Stadium", 
                                    null=True, blank=True)
    match_date = models.DateField(verbose_name="Match Date")
    match_referee = models.CharField(max_length=255, verbose_name="Match Referee", null=True, blank=True)
    umpire1 = models.CharField(max_length=255, verbose_name="Umpire 1")
    umpire2 = models.CharField(max_length=255, verbose_name="Umpire 2")
    match_winner = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="Match Winner", 
                                    null=True, blank=True)  # Made optional
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['match_date']),
            models.Index(fields=['season']),
        ]
    
    def __str__(self):
        winner_name = self.match_winner.team_name if self.match_winner else "No winner yet"
        return f"{self.match_date} - {winner_name}"
    
def get_teams_and_players(self):
    match_teams = self.teams.select_related('team').prefetch_related(
        Prefetch(
            'team__player_associations',
            queryset=PlayerTeamSeason.objects.filter(season=self.season).select_related('player'),
            to_attr='season_players'
        )
    ).all()
    
    teams_and_players = {}
    for match_team in match_teams:
        teams_and_players[match_team.team.team_name] = [
            player_assoc.player.name for player_assoc in match_team.team.season_players
        ]
    return teams_and_players

class MatchTeam(models.Model):
    match = models.ForeignKey(MatchInfo, on_delete=models.CASCADE, related_name='teams')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_home_team = models.BooleanField(default=False, verbose_name="Is Home Team")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['match', 'team'], name='unique_match_team')
        ]
    
    def __str__(self):
        ha = "Home" if self.is_home_team else "Away"
        return f"{self.team.team_name} ({ha}) in {self.match}"


class Player(models.Model):
    name = models.CharField(max_length=255, unique=True)
    identifier = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def get_matches_and_teams(self):
        # Get all associations of the player
        player_associations = PlayerTeamSeason.objects.filter(player=self).select_related('team', 'season')
        
        # Fetch matches where the player's team participated
        matches = MatchTeam.objects.filter(team__in=[assoc.team for assoc in player_associations]) \
                                   .select_related('match', 'match__season', 'team')

        match_details = []
        for match_team in matches:
            match = match_team.match
            match_details.append({
                "date": match.match_date,
                "season": match.season.year,
                "stadium": match.match_stadium.stadium_name if match.match_stadium else "Unknown",
                "opponent": [
                    opponent.team.team_name for opponent in match.teams.exclude(team=match_team.team)
                ],
                "is_home_team": match_team.is_home_team,
            })

        teams = list({assoc.team.team_name for assoc in player_associations})
        return {
            "teams_played_for": teams,
            "matches": match_details
        }


class PlayerTeamSeason(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='team_associations')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='player_associations')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='player_team_associations')

    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['player', 'team', 'season'], name='unique_player_team_season')
        ]

        indexes = [
            models.Index(fields=['player', 'season']),
            models.Index(fields=['team', 'season']),
        ]
    def __str__(self):
        return f"{self.player.name} - {self.team.team_name} ({self.season.year})"