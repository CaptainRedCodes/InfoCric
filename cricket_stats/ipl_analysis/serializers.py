from rest_framework import serializers
from .models import Season,Team,Player,MatchInfo,PlayerTeamSeason,StadiumInfo,MatchInfo,Player

#Serializers allow complex data such as querysets and model instances 
#to be converted to native Python datatypes that can then be easily rendered into JSON, XML or other content types. 
#match meta
class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model=Season
        fields='__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model=Team
        fields='__all__'

class StadiumInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=StadiumInfo
        fields=['id','stadium_name','city']

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Player
        fields='__all__'

class MatchInfoSerializer(serializers.ModelSerializer):
    match_city = serializers.CharField(source='match_city.city')
    match_stadium = serializers.CharField(source='match_city.stadium_name')
    match_winner = serializers.StringRelatedField()
    season = serializers.StringRelatedField()

    class Meta:
        model = MatchInfo
        fields = [
            'id', 'match_city', 'match_stadium', 'match_date', 
            'match_referee', 'umpire1', 'umpire2', 'match_winner', 
            'season'
        ]