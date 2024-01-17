from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from apps.player.api.serializers import PlayerListSerializer, PlayerSerializer
from apps.player.models import Player, PlayerList, UserPlayerList


class UserPlayerListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = self.request.user

        user_player_lists = UserPlayerList.objects.filter(user=user)
        if user_player_lists.exists():
            player_lists = [
                user_player_list.player_list for user_player_list in user_player_lists
            ]
            player_lists_serializer = PlayerListSerializer(player_lists, many=True)

            return Response(
                {"player_lists": player_lists_serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Player lists not found"}, status=status.HTTP_404_NOT_FOUND
            )


class PlayerListDetailAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id):
        user = self.request.user

        player_list = PlayerList.objects.filter(id=id).first()

        if (
            player_list
            and UserPlayerList.objects.filter(
                user=user, player_list=player_list
            ).exists()
        ):
            result = {
                "id": player_list.id,
                "title": player_list.title,
            }

            players = Player.objects.filter(player_list=player_list)
            players_serializer = PlayerSerializer(players, many=True)

            result["players"] = players_serializer.data

            return Response(
                {"player_list": result},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Player list not found"}, status=status.HTTP_404_NOT_FOUND
            )


class CreateUserPlayerListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = self.request.user

        data = self.request.data
        with transaction.atomic():
            player_list = PlayerList(title=data["title"], players=len(data["players"]))
            player_list.full_clean()
            player_list.save()

            user_player_list = UserPlayerList(user=user, player_list=player_list)
            user_player_list.full_clean()
            user_player_list.save()

            for player_data in data["players"]:
                player = Player(
                    player_list=player_list,
                )
                for key, value in player_data.items():
                    setattr(player, key, value)

                player.full_clean()
                player.save()

            return Response(
                {"success": "List created"},
                status=status.HTTP_201_CREATED,
            )


class EditUserPlayerListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        user = self.request.user

        data = self.request.data
        player_list = PlayerList.objects.filter(id=data["id"]).first()

        if (
            player_list
            and UserPlayerList.objects.filter(
                user=user, player_list=player_list
            ).exists()
        ):
            with transaction.atomic():
                player_list.title = data["title"]
                player_list.players = len(data["players"])
                player_list.full_clean()
                player_list.save()

                Player.objects.filter(player_list=player_list).delete()

                for player_data in data["players"]:
                    player = Player(
                        player_list=player_list,
                    )
                    for key, value in player_data.items():
                        setattr(player, key, value)

                    player.full_clean()
                    player.save()

                return Response(
                    {"success": "List edited"},
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(
                {"error": "Player list not found"}, status=status.HTTP_404_NOT_FOUND
            )


class DeleteUserPlayerListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, id, format=None):
        user = self.request.user

        player_list = PlayerList.objects.filter(id=id).first()

        if (
            player_list
            and UserPlayerList.objects.filter(
                user=user, player_list=player_list
            ).exists()
        ):
            player_list.delete()
            return Response(
                {"success": "List deleted"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Player list not found"}, status=status.HTTP_404_NOT_FOUND
            )
