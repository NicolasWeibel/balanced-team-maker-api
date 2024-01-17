from rest_framework import serializers
from apps.draw.models import Draw


class DrawSerializer(serializers.ModelSerializer):
    players = serializers.IntegerField(source="player_list.players")
    teams = serializers.IntegerField(source="team_list.teams")

    class Meta:
        model = Draw
        fields = ("id", "title", "slug", "last_modified", "type", "players", "teams")
