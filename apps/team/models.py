from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

User = settings.AUTH_USER_MODEL
MAX_TEAM_LISTS_PER_USER = 20
MAX_TEAMS_PER_LIST = 100
MIN_TEAMS_PER_LIST = 1


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
    teams = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_TEAMS_PER_LIST),
            MaxValueValidator(MAX_TEAMS_PER_LIST),
        ]
    )

    class Meta:
        verbose_name = "Team List"
        verbose_name_plural = "Team Lists"

    def __str__(self):
        return f"{self.title} / {self.teams} teams"


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

    team_list = models.ForeignKey(TeamList, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

        unique_together = ("position", "team_list")

    def __str__(self):
        return f"{self.name} / {self.position}°"
