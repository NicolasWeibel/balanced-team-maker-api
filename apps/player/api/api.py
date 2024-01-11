from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from apps.player.api.serializers import PlayerListSerializer
from apps.player.models import Player, PlayerList, UserPlayerList


class UserPlayerListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = self.request.user
        if UserPlayerList.objects.filter(user=user).exists():
            user_player_lists = UserPlayerList.objects.filter(user=user)

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
        if PlayerList.objects.filter(user=user, id=id).exists():
            player_list = UserPlayerList.objects.filter(user=user, id=id)

            player_list_serializer = PlayerListSerializer(player_list)

            return Response(
                {"player_lists": player_list_serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Player lists not found"}, status=status.HTTP_404_NOT_FOUND
            )


class CreateUserPlayerListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = self.request.user

        data = self.request.data

        try:
            with transaction.atomic():
                player_list = PlayerList.objects.create(
                    title=data["title"], players=len(data["players"])
                )
                user_player_list = UserPlayerList(user=user, player_list=player_list)
                user_player_list.full_clean()
                user_player_list.save()

                for player_data in data["players"]:
                    player = Player(
                        name=player_data.name,
                        position=player_data.position,
                        player_list=player_list,
                        gender=player_data.gender,
                        stars=player_data.stars,
                        attack=player_data.attack,
                        defense=player_data.defense,
                        resistance=player_data.resistance,
                    )
                    player.full_clean()
                    player.save()

                return Response(
                    {"success": "List created"},
                    status=status.HTTP_200_OK,
                )
        except IntegrityError as e:
            return Response(
                {"error": e.message},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class EditUserPlayerListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        user = self.request.user

        data = self.request.data
        player_list = PlayerList.objects.filter(id=data["id"])

        if UserPlayerList.objects.filter(user=user, player_list=player_list).exists():
            try:
                with transaction.atomic():
                    player_list.update(
                        title=data["title"], players=len(data["players"])
                    )

                    Player.objects.filter(player_list=player_list).delete()

                    for player_data in data["players"]:
                        player = Player(
                            name=player_data["name"],
                            position=player_data["position"],
                            player_list=player_list,
                            gender=player_data["gender"],
                            stars=player_data["stars"],
                            attack=player_data["attack"],
                            defense=player_data["defense"],
                            resistance=player_data["resistance"],
                        )
                        player.full_clean()
                        player.save()

                    return Response(
                        {"success": "List edited"},
                        status=status.HTTP_200_OK,
                    )
            except IntegrityError as e:
                return Response(
                    {"error": e.message},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(
                {"error": "Player list not found"}, status=status.HTTP_404_NOT_FOUND
            )


class DeleteUserPlayerListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, format=None):
        user = self.request.user

        data = self.request.data
        player_list = PlayerList.objects.filter(id=data["id"])

        if UserPlayerList.objects.filter(user=user, player_list=player_list).exists():
            player_list.delete()
            return Response(
                {"success": "List deleted"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Player list not found"}, status=status.HTTP_404_NOT_FOUND
            )
