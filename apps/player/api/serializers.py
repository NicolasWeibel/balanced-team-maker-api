from rest_framework import serializers
from apps.player.models import Player, PlayerList, UserPlayerList
from apps.user.api.serializers import UserSerializer


class PlayerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerList
        fields = [
            "id",
            "title",
            "players",
        ]


class UserPlayerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    player_list = PlayerListSerializer()

    class Meta:
        model = UserPlayerList
        fields = [
            "id",
            "user",
            "player_list",
        ]


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            "id",
            "name",
            "position",
            "gender",
            "stars",
            "defense",
            "attack",
            "resistance",
        ]
