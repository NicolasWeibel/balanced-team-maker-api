from django.urls import path

from apps.draw.api.api import (
    CreateDrawAPIView,
    DeleteDrawAPIView,
    DrawlDetailAPIView,
    EditDrawAPIView,
    UserDrawListAPIView,
)

urlpatterns = [
    path("list", UserDrawListAPIView.as_view(), name="draw_list_api"),
    path("detail/<id>", DrawlDetailAPIView.as_view(), name="draw_detail_api"),
    path(
        "create",
        CreateDrawAPIView.as_view(),
        name="create_draw_api",
    ),
    path(
        "edit",
        EditDrawAPIView.as_view(),
        name="edit_draw_api",
    ),
    path(
        "delete/<id>",
        DeleteDrawAPIView.as_view(),
        name="delete_draw_api",
    ),
]
