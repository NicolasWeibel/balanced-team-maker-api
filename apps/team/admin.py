from django.contrib import admin

from apps.team.models import MAX_TEAMS_PER_LIST, Team, TeamList, UserTeamList


class UserTeamListInline(admin.TabularInline):
    model = UserTeamList
    extra = 0
    max_num = 1
    show_change_link = True


class TeamInline(admin.TabularInline):
    model = Team
    extra = 0
    max_num = MAX_TEAMS_PER_LIST
    show_change_link = True


@admin.register(TeamList)
class TeamListAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {"fields": ("title",)},
        ),
        (
            "Teams",
            {"fields": ("teams",)},
        ),
    )

    list_display = (
        "id",
        "title",
        "teams",
    )
    search_fields = (
        "title",
        "teams",
    )

    list_filter = ("teams",)

    inlines = [TeamInline, UserTeamListInline]


@admin.register(UserTeamList)
class UserTeamListAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "User",
            {"fields": ("user",)},
        ),
        (
            "Team List",
            {"fields": ("team_list",)},
        ),
    )

    list_display = (
        "id",
        "user",
        "team_list",
    )
    search_fields = (
        "user",
        "team_list",
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "position",
                    "team_list",
                )
            },
        ),
    )

    list_display = (
        "id",
        "name",
        "position",
        "team_list",
    )
    search_fields = (
        "name",
        "team_list",
    )

    list_filter = ("team_list",)
