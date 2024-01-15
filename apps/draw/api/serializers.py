from rest_framework import serializers
from apps.draw.models import Draw
from apps.player.api.serializers import PlayerListSerializer
from apps.team.api.serializers import TeamListSerializer
from apps.user.api.serializers import UserSerializer


class DrawListSerializer(serializers.ModelSerializer):
    players = serializers.IntegerField(source="player_list.players")
    teams = serializers.IntegerField(source="team_list.teams")

    class Meta:
        model = Draw
        fields = ("id", "title", "slug", "last_modified", "type", "players", "teams")
