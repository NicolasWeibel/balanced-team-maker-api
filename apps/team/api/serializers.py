from rest_framework import serializers
from apps.team.models import Team, TeamList, UserTeamList
from apps.user.api.serializers import UserSerializer


class TeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamList
        fields = [
            "id",
            "title",
            "teams",
        ]


class UserTeamListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    team_list = TeamListSerializer()

    class Meta:
        model = UserTeamList
        fields = [
            "id",
            "user",
            "team_list",
        ]


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "position",
        ]
