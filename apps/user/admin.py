from django.contrib import admin

from apps.player.admin import UserPlayerListInline
from apps.user.models import User
from apps.team.admin import UserTeamListInline


# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("username", "email")}),
        (
            "Details",
            {
                "fields": (
                    "language",
                    "player_lists",
                    "team_lists",
                    "draws",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "language",
        "is_active",
        "is_staff",
        "last_login",
    )
    search_fields = (
        "username",
        "email",
        "language",
    )

    list_filter = ("is_active", "is_staff")

    date_hierarchy = "last_login"

    inlines = [UserPlayerListInline, UserTeamListInline]
