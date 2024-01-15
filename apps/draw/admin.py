from django.contrib import admin

from apps.draw.models import Draw


@admin.register(Draw)
class DrawAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                )
            },
        ),
        (
            "Details",
            {
                "fields": (
                    "type",
                    "user",
                    "player_list",
                    "team_list",
                    "last_modified",
                )
            },
        ),
    )

    list_display = (
        "title",
        "slug",
        "type",
        "user",
        "player_list",
        "team_list",
        "last_modified",
    )
    search_fields = (
        "title",
        "user",
    )

    list_filter = ("type",)

    date_hierarchy = "last_modified"

    readonly_fields = ("last_modified",)
