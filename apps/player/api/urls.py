from django.urls import path

from apps.player.api.api import (
    CreateUserPlayerListAPIView,
    DeleteUserPlayerListAPIView,
    EditUserPlayerListAPIView,
    PlayerListDetailAPIView,
    UserPlayerListAPIView,
)

urlpatterns = [
    path("list", UserPlayerListAPIView.as_view(), name="player_list_api"),
    path(
        "list/create",
        CreateUserPlayerListAPIView.as_view(),
        name="create_player_list_api",
    ),
    path(
        "list/edit",
        EditUserPlayerListAPIView.as_view(),
        name="create_player_list_api",
    ),
    path(
        "list/delete",
        DeleteUserPlayerListAPIView.as_view(),
        name="create_player_list_api",
    ),
    path(
        "detail/<id>", PlayerListDetailAPIView.as_view(), name="player_list_detail_api"
    ),
]
