from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.draw.slug import unique_slugify

from apps.player.models import PlayerList
from apps.team.models import TeamList

User = settings.AUTH_USER_MODEL
MAX_DRAWS_PER_USER = 1000


def validate_max_draws_per_user(user):
    if Draw.objects.filter(user=user).count() >= MAX_DRAWS_PER_USER:
        raise ValidationError(
            (f"User has reached the maximum limit of draws ({MAX_DRAWS_PER_USER})."),
        )


class Draw(models.Model):
    TYPE_CHOICES = (
        ("n", "Normal"),
        ("g", "Gender"),
        ("s", "Skill Level"),
        ("a", "Advanced"),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, validators=[validate_max_draws_per_user]
    )
    player_list = models.ForeignKey(PlayerList, on_delete=models.CASCADE)
    team_list = models.ForeignKey(TeamList, on_delete=models.CASCADE)

    last_modified = models.DateTimeField()

    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default="n")

    class Meta:
        verbose_name = "Draw"
        verbose_name_plural = "Draws"

    def save(self, **kwargs):
        if self._state.adding:
            # Create unique slug
            slug_str = self.title
            unique_slugify(self, slug_str)

        # Update last_modified
        self.last_modified = timezone.now()

        super(Draw, self).save(**kwargs)

    def __str__(self):
        return f"{self.title} / {self.player_list.players} players in {self.team_list.teams} teams"
