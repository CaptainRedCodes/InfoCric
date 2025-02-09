from django.core.management.base import BaseCommand
from django.db import transaction
from ipl_analysis.models import Team, MatchTeam, PlayerTeamSeason, MatchInfo,StadiumInfo

class Command(BaseCommand):
    help = "Merge duplicate teams and update team names"

    # def handle(self, *args, **kwargs):
    #     # First, let's print all existing teams
    #     self.stdout.write("Current teams in database:")
    #     for team in Team.objects.all().order_by('id'):
    #         self.stdout.write(f"ID: {team.id} - Name: {team.team_name}")

    #     # Updated merge mapping with correct IDs
    #     team_merge_map = {
    #         2: (15, "Royal Challengers Bengaluru"),   # RCB -> RCB (renamed)
    #         19: (3, "Rising Pune Supergiant"),        # Rising Pune Supergiants -> Rising Pune Supergiant
    #         7: (12, "Punjab Kings"),                  # Kings XI Punjab -> Punjab Kings
    #         8: (11, "Delhi Capitals"),                # Delhi Daredevils -> Delhi Capitals
    #     }

    #     try:
    #         with transaction.atomic():
    #             for old_team_id, (new_team_id, new_name) in team_merge_map.items():
    #                 old_team = Team.objects.get(pk=old_team_id)
    #                 new_team = Team.objects.get(pk=new_team_id)

    #                 self.stdout.write(f"\nProcessing merge: {old_team.team_name} -> {new_name}")

    #                 # Update the new team's name
    #                 new_team.team_name = new_name
    #                 new_team.save()

    #                 # Update MatchTeam references
    #                 match_teams_updated = MatchTeam.objects.filter(team=old_team).update(team=new_team)
    #                 self.stdout.write(f"Updated {match_teams_updated} MatchTeam records")

    #                 # Update match winner references
    #                 matches_updated = MatchInfo.objects.filter(match_winner=old_team).update(match_winner=new_team)
    #                 self.stdout.write(f"Updated {matches_updated} MatchInfo records")

    #                 # Handle PlayerTeamSeason merging
    #                 old_associations = PlayerTeamSeason.objects.filter(team=old_team)
    #                 association_count = 0
    #                 for association in old_associations:
    #                     if association.season:
    #                         PlayerTeamSeason.objects.get_or_create(
    #                             player=association.player,
    #                             team=new_team,
    #                             season=association.season
    #                         )
    #                         association_count += 1
    #                     else:
    #                         self.stdout.write(
    #                             self.style.WARNING(
    #                                 f"Skipping player {association.player.name} due to missing season"
    #                             )
    #                         )

    #                 self.stdout.write(f"Processed {association_count} PlayerTeamSeason records")
                    
    #                 # Delete old associations
    #                 old_associations.delete()
                    
    #                 # Delete the old team
    #                 old_team.delete()
    #                 self.stdout.write(
    #                     self.style.SUCCESS(
    #                         f"Successfully merged '{old_team.team_name}' into '{new_name}'"
    #                     )
    #                 )

    #         self.stdout.write(self.style.SUCCESS("\nAll team merges completed successfully"))
            
    #         # Print final team list
    #         self.stdout.write("\nFinal team list:")
    #         for team in Team.objects.all().order_by('id'):
    #             self.stdout.write(f"ID: {team.id} - Name: {team.team_name}")

    #     except Exception as e:
    #         self.stdout.write(
    #             self.style.ERROR(f"An error occurred during the merge process: {str(e)}")
    #         )

    def handle(self, *args, **kwargs):
            # First, display current stadiums
            self.stdout.write("Current stadiums in database:")
            for stadium in StadiumInfo.objects.all().order_by('id'):
                self.stdout.write(f"ID: {stadium.id} - Name: {stadium.stadium_name} - City: {stadium.city}")

            # Stadium merging and renaming map
            stadium_merge_map = {
                # Rajiv Gandhi Stadium variants
                1: (13, "Rajiv Gandhi International Stadium", "Hyderabad"),  # Merge Uppal variant
                37: (13, "Rajiv Gandhi International Stadium", "Hyderabad"),  # Merge Uppal variant
                
                # M Chinnaswamy Stadium variants
                8: (5, "M Chinnaswamy Stadium", "Bengaluru"),  # Merge Bangalore variant
                35: (5, "M Chinnaswamy Stadium", "Bengaluru"),  # Merge Bengaluru variant
                
                # Wankhede Stadium variants
                22: (6, "Wankhede Stadium", "Mumbai"),
                
                # MA Chidambaram Stadium variants
                21: (14, "MA Chidambaram Stadium", "Chennai"),
                43: (14, "MA Chidambaram Stadium", "Chennai"),
                
                # Punjab Cricket Association Stadium variants
                10: (12, "Punjab Cricket Association IS Bindra Stadium", "Chandigarh"),
                33: (12, "Punjab Cricket Association IS Bindra Stadium", "Chandigarh"),
                42: (12, "Punjab Cricket Association IS Bindra Stadium", "Chandigarh"),
                
                # Dr DY Patil Sports Academy variants
                29: (31, "Dr DY Patil Sports Academy", "Navi Mumbai"),
                44: (31, "Dr DY Patil Sports Academy", "Navi Mumbai"),
                
                # Dubai International Cricket Stadium
                19: (27, "Dubai International Cricket Stadium", "Dubai"),
                
                # Sharjah Cricket Stadium
                20: (26, "Sharjah Cricket Stadium", "Sharjah"),
                
                # Eden Gardens
                32: (7, "Eden Gardens", "Kolkata"),
                
                # Arun Jaitley Stadium (formerly Feroz Shah Kotla)
                9: (16, "Arun Jaitley Stadium", "Delhi"),
                24: (16, "Arun Jaitley Stadium", "Delhi"),
                
                # Maharashtra Cricket Association Stadium
                30: (2, "Maharashtra Cricket Association Stadium", "Pune"),
                
                # Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium
                41: (17, "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium", "Visakhapatnam"),
                
                # Sawai Mansingh Stadium
                38: (15, "Sawai Mansingh Stadium", "Jaipur"),
                
                # Himachal Pradesh Cricket Association Stadium
                57: (39, "Himachal Pradesh Cricket Association Stadium", "Dharamsala"),
                
                # Zayed Cricket Stadium
                18: (25, "Zayed Cricket Stadium", "Abu Dhabi"),
                
                # Brabourne Stadium
                53: (28, "Brabourne Stadium", "Mumbai"),
            }

            try:
                with transaction.atomic():
                    for old_stadium_id, (new_stadium_id, new_name, new_city) in stadium_merge_map.items():
                        try:
                            old_stadium = StadiumInfo.objects.get(pk=old_stadium_id)
                            new_stadium = StadiumInfo.objects.get(pk=new_stadium_id)

                            self.stdout.write(f"\nProcessing merge: {old_stadium.stadium_name} -> {new_name}")

                            # Update the new stadium's information
                            new_stadium.stadium_name = new_name
                            new_stadium.city = new_city
                            new_stadium.save()

                            # Update MatchInfo references
                            matches_stadium_updated = MatchInfo.objects.filter(
                                match_stadium=old_stadium
                            ).update(match_stadium=new_stadium)
                            
                            matches_city_updated = MatchInfo.objects.filter(
                                match_city=old_stadium
                            ).update(match_city=new_stadium)

                            self.stdout.write(
                                f"Updated {matches_stadium_updated} match stadium references and "
                                f"{matches_city_updated} match city references"
                            )

                            # Optionally delete the old stadium
                            old_stadium.delete()

                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Successfully merged stadium '{old_stadium.stadium_name}' into '{new_name}' "
                                    f"in {new_city}"
                                )
                            )
                        except StadiumInfo.DoesNotExist:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"Stadium with ID {old_stadium_id} or {new_stadium_id} not found. Skipping."
                                )
                            )

                self.stdout.write(self.style.SUCCESS("\nAll stadium merges completed successfully"))
                
                # Print final stadium list
                self.stdout.write("\nFinal stadium list:")
                for stadium in StadiumInfo.objects.all().order_by('id'):
                    self.stdout.write(
                        f"ID: {stadium.id} - Name: {stadium.stadium_name} - City: {stadium.city}"
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"An error occurred during the merge process: {str(e)}")
                )