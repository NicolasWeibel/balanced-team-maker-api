from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL
MAX_PLAYER_LISTS_PER_USER = 20
MAX_PLAYERS_PER_LIST = 100


def validate_max_player_lists_per_user(user):
    if UserPlayerList.objects.filter(user=user).count() >= MAX_PLAYER_LISTS_PER_USER:
        raise ValidationError(
            (
                f"User has reached the maximum limit of lists ({MAX_PLAYER_LISTS_PER_USER})."
            ),
        )


def validate_max_players_per_list(player_list):
    if Player.objects.filter(player_list=player_list).count() >= MAX_PLAYERS_PER_LIST:
        raise ValidationError(
            (
                f"List has reached the maximum limit of players ({MAX_PLAYERS_PER_LIST})."
            ),
        )


class PlayerList(models.Model):
    title = models.CharField(max_length=255, blank=True)
    players = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Player List"
        verbose_name_plural = "Player Lists"

    def get_player_count(self):
        players = Player.objects.filter(player_list=self).count()
        return players

    def __str__(self):
        return f"{self.title} / {self.players} players"


class UserPlayerList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, validators=[validate_max_player_lists_per_user]
    )
    player_list = models.ForeignKey(PlayerList, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "User Player List"
        verbose_name_plural = "User Player Lists"


class Player(models.Model):
    GENDER_CHOICES = (
        ("m", "Male"),
        ("f", "Female"),
    )

    STAR_CHOICES = [
        (0.0, "0"),
        (0.5, "0.5"),
        (1.0, "1"),
        (1.5, "1.5"),
        (2.0, "2"),
        (2.5, "2.5"),
        (3.0, "3"),
        (3.5, "3.5"),
        (4.0, "4"),
        (4.5, "4.5"),
        (5.0, "5"),
    ]

    name = models.CharField(max_length=255)
    position = models.PositiveSmallIntegerField()

    player_list = models.ForeignKey(
        PlayerList, on_delete=models.CASCADE, validators=[validate_max_players_per_list]
    )

    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, default="n"
    )
    stars = models.DecimalField(
        max_digits=2, decimal_places=1, choices=STAR_CHOICES, null=True, blank=True
    )
    attack = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(99)],
        null=True,
        blank=True,
    )
    defense = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(99)],
        null=True,
        blank=True,
    )
    resistance = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(99)],
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"

        unique_together = ("position", "player_list")

    def __str__(self):
        return f"{self.name} / {self.position}°"
