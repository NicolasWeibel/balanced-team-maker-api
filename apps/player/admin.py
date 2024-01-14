from django.contrib import admin

from apps.player.models import MAX_PLAYERS_PER_LIST, Player, PlayerList, UserPlayerList


class UserPlayerListInline(admin.TabularInline):
    model = UserPlayerList
    extra = 0
    max_num = 1
    show_change_link = True


class PlayerInline(admin.TabularInline):
    model = Player
    extra = 0
    max_num = MAX_PLAYERS_PER_LIST
    show_change_link = True


@admin.register(PlayerList)
class PlayerListAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {"fields": ("title",)},
        ),
        (
            "Players",
            {"fields": ("players",)},
        ),
    )

    list_display = (
        "id",
        "title",
        "players",
    )
    search_fields = (
        "title",
        "players",
    )

    list_filter = ("players",)

    inlines = [PlayerInline, UserPlayerListInline]


@admin.register(UserPlayerList)
class UserPlayerListAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "User",
            {"fields": ("user",)},
        ),
        (
            "Player List",
            {"fields": ("player_list",)},
        ),
    )

    list_display = (
        "id",
        "user",
        "player_list",
    )
    search_fields = (
        "user",
        "player_list",
    )


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "position",
                    "player_list",
                )
            },
        ),
        (
            "Gender",
            {"fields": ("gender",)},
        ),
        (
            "Stars",
            {"fields": ("stars",)},
        ),
        (
            "Sport",
            {
                "fields": (
                    "attack",
                    "defense",
                    "resistance",
                )
            },
        ),
    )

    list_display = (
        "id",
        "name",
        "position",
        "player_list",
    )
    search_fields = (
        "name",
        "player_list",
    )

    list_filter = (
        "player_list",
        "gender",
        "stars",
        "attack",
        "defense",
        "resistance",
    )
