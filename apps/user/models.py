from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from simple_history.models import HistoricalRecords

# Create your models here.


class UserManager(BaseUserManager):
    def _create_user(
        self,
        email,
        is_staff,
        is_superuser,
        password=None,
        **extra_fields,
    ):
        if not email:
            raise ValueError("Users must have an email address")

        if "language" in extra_fields and extra_fields["language"] == "":
            extra_fields["language"] = "en"

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, False, False, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return self._create_user(email, True, True, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField("Email", max_length=255, unique=True)

    language = models.CharField(max_length=10, default="en", blank=True)

    player_lists = models.IntegerField(default=0, blank=True)
    team_lists = models.IntegerField(default=0, blank=True)
    draws = models.IntegerField(default=0, blank=True)

    date_joined = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    historical = HistoricalRecords()
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "language"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
