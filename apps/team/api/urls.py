from django.urls import path

from apps.team.api.api import (
    CreateUserTeamListAPIView,
    DeleteUserTeamListAPIView,
    EditUserTeamListAPIView,
    TeamListDetailAPIView,
    UserTeamListAPIView,
)

urlpatterns = [
    path("list", UserTeamListAPIView.as_view(), name="team_list_api"),
    path(
        "list/create",
        CreateUserTeamListAPIView.as_view(),
        name="create_team_list_api",
    ),
    path(
        "list/edit",
        EditUserTeamListAPIView.as_view(),
        name="edit_team_list_api",
    ),
    path(
        "list/delete/<id>",
        DeleteUserTeamListAPIView.as_view(),
        name="delete_team_list_api",
    ),
    path("detail/<id>", TeamListDetailAPIView.as_view(), name="team_list_detail_api"),
]
