from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL
MAX_TEAM_LISTS_PER_USER = 20
MAX_TEAMS_PER_LIST = 100


def validate_max_team_lists_per_user(user):
    if UserTeamList.objects.filter(user=user).count() >= MAX_TEAM_LISTS_PER_USER:
        raise ValidationError(
            (
                f"User has reached the maximum limit of lists ({MAX_TEAM_LISTS_PER_USER})."
            ),
        )


def validate_max_teams_per_list(team_list):
    if Team.objects.filter(team_list=team_list).count() >= MAX_TEAMS_PER_LIST:
        raise ValidationError(
            (f"List has reached the maximum limit of teams ({MAX_TEAMS_PER_LIST})."),
        )


class TeamList(models.Model):
    title = models.CharField(max_length=255, blank=True)
    teams = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Team List"
        verbose_name_plural = "Team Lists"

    def get_team_count(self):
        teams = Team.objects.filter(team_list=self).count()
        return teams


class UserTeamList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, validators=[validate_max_team_lists_per_user]
    )
    team_list = models.ForeignKey(TeamList, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "User Team List"
        verbose_name_plural = "User Team Lists"


class Team(models.Model):
    name = models.CharField(max_length=255)
    position = models.PositiveSmallIntegerField()

    team_list = models.ForeignKey(
        TeamList, on_delete=models.CASCADE, validators=[validate_max_teams_per_list]
    )

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

        unique_together = ("position", "team_list")
