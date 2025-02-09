# your_app/management/commands/import_match_data.py
import json
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from ipl_analysis.models import Season, Team, StadiumInfo, MatchInfo, MatchTeam, Player, PlayerTeamSeason


class Command(BaseCommand):
    help = 'Imports IPL match data from JSON files into the database'

    def handle(self, *args, **kwargs):
        
        json_folder_path = r'C:\Users\svmra\OneDrive\Documents\projects\cric _analysus\jsonfile'
        
        if not os.path.exists(json_folder_path):
            self.stderr.write(self.style.ERROR(f"JSON folder path does not exist: {json_folder_path}"))
            return

        # Get all JSON files in the directory
        json_files = [f for f in os.listdir(json_folder_path) if f.endswith(".json")]
        
        if not json_files:
            self.stdout.write(self.style.WARNING("No JSON files found in the directory."))
            return

        for json_file in json_files:
            file_path = os.path.join(json_folder_path, json_file)
            self.stdout.write(self.style.NOTICE(f"Processing file: {file_path}"))
            self.import_match(file_path)

    def import_match(self, file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            # Extract match info
            season_year = data['info'].get('season')
            stadium_name = data['info'].get('venue')
            teams = data['info'].get('teams', [])
            
            if len(teams) != 2:
                self.stderr.write(self.style.ERROR(f"Invalid data in {file_path}: expected exactly 2 teams"))
                return

            match_city = data['info'].get('city', 'Unknown')
            match_date = data['info']['dates'][0]
            match_referee = data['info'].get('officials', {}).get('match_referees', [None])[0]
            umpires = data['info'].get('officials', {}).get('umpires', [])
            umpire1 = umpires[0] if len(umpires) > 0 else 'Unknown'
            umpire2 = umpires[1] if len(umpires) > 1 else 'Unknown'

            outcome = data['info'].get('outcome', {})
            match_winner_team_name = outcome.get('winner', None)
            if outcome.get('result') == 'tie':
                match_winner_team_name = f"Tie: Eliminator Winner - {outcome.get('eliminator', 'Unknown')}"

            team1_name, team2_name = teams
            registry_data = data['info'].get('registry', {}).get('people', {})

            try:
                with transaction.atomic():
                    # Handle Players
                    if Player.objects.exists():
                        existing_player_names = set(Player.objects.values_list('name', flat=True))
                    else:
                        existing_player_names = set()
                    
                    new_players = [
                        Player(name=player_name, identifier=identifier)
                        for player_name, identifier in registry_data.items()
                        if player_name not in existing_player_names
                    ]
                    if new_players:
                        Player.objects.bulk_create(new_players)

                    # Create or fetch season
                    season, _ = Season.objects.get_or_create(year=season_year)

                    # Create or fetch stadium with city
                    stadium, _ = StadiumInfo.objects.get_or_create(
                        stadium_name=stadium_name,
                        city=match_city
                    )

                    # Create or fetch teams
                    team1, _ = Team.objects.get_or_create(team_name=team1_name)
                    team2, _ = Team.objects.get_or_create(team_name=team2_name)

                    # Determine match winner
                    match_winner = None
                    if match_winner_team_name:
                        match_winner = Team.objects.filter(team_name=match_winner_team_name).first()

                    # Create match info - Now using the stadium instance for both city and stadium
                    try:
                        match = MatchInfo.objects.create(
                            match_city=stadium,  # Use the same stadium instance for city
                            match_stadium=stadium,
                            match_date=datetime.fromisoformat(match_date),
                            match_referee=match_referee,
                            umpire1=umpire1,
                            umpire2=umpire2,
                            match_winner=match_winner,
                            season=season
                        )
                    except Exception as e:
                        self.stderr.write(self.style.ERROR(f"Error creating match: {str(e)}"))
                        raise

                    # Link teams to match
                    try:
                        MatchTeam.objects.bulk_create([
                            MatchTeam(match=match, team=team1, is_home_team=True),
                            MatchTeam(match=match, team=team2, is_home_team=False)
                        ])
                    except Exception as e:
                        self.stderr.write(self.style.ERROR(f"Error linking teams to match: {str(e)}"))
                        raise

                    # Extract and create player-team associations
                    try:
                        players_in_match = set()
                        for team_name, team_obj in [(team1_name, team1), (team2_name, team2)]:
                            team_players = data['info'].get('players', {}).get(team_name, [])
                            for player_name in team_players:
                                players_in_match.add((player_name, team_obj.id))

                        # Create PlayerTeamSeason records
                        player_team_seasons = []
                        for player_name, team_id in players_in_match:
                            player = Player.objects.get(name=player_name)
                            player_team_seasons.append(
                                PlayerTeamSeason(
                                    player=player,
                                    team_id=team_id,
                                    season=season
                                )
                            )
                        
                        if player_team_seasons:
                            PlayerTeamSeason.objects.bulk_create(
                                player_team_seasons,
                                ignore_conflicts=True
                            )
                    except Exception as e:
                        self.stderr.write(self.style.ERROR(f"Error creating player-team associations: {str(e)}"))
                        raise

                    self.stdout.write(self.style.SUCCESS(f"Successfully imported data from {file_path}"))

            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Transaction error: {str(e)}"))
                raise

        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR(f"JSON parsing error in file: {file_path}"))
        except KeyError as e:
            self.stderr.write(self.style.ERROR(f"Missing key in file {file_path}: {e}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error importing {file_path}: {str(e)}"))