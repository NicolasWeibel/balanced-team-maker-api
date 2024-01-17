from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from apps.draw.api.serializers import DrawSerializer
from apps.draw.models import Draw
from apps.player.api.serializers import PlayerSerializer
from apps.player.models import Player, PlayerList

from apps.team.api.serializers import TeamSerializer
from apps.team.models import Team, TeamList


class UserDrawListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = self.request.user
        if Draw.objects.filter(user=user).exists():
            draws = Draw.objects.filter(user=user)

            draws_serializer = DrawSerializer(draws, many=True)

            return Response(
                {"draws": draws_serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Draws not found"}, status=status.HTTP_404_NOT_FOUND
            )


class DrawlDetailAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id, format=None):
        user = self.request.user

        draw = Draw.objects.filter(user=user, id=id).first()
        if draw:
            draw_serializer = DrawSerializer(draw)
            result = draw_serializer.data

            players = Player.objects.filter(player_list=draw.player_list)
            players_serializer = PlayerSerializer(players, many=True)
            result["player_list"] = players_serializer.data

            teams = Team.objects.filter(team_list=draw.team_list)
            teams_serializer = TeamSerializer(teams, many=True)
            result["team_list"] = teams_serializer.data

            return Response(
                {"draw": result},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Draw not found"}, status=status.HTTP_404_NOT_FOUND
            )


class CreateDrawAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = self.request.user
        data = self.request.data

        with transaction.atomic():
            # Create player list
            player_list = PlayerList(players=len(data["player_list"]))
            player_list.full_clean()
            player_list.save()

            for player_data in data["player_list"]:
                player = Player(
                    player_list=player_list,
                )
                for key, value in player_data.items():
                    setattr(player, key, value)

                player.full_clean()
                player.save()
            data.pop("player_list")

            # Create team list
            team_list = TeamList(teams=len(data["team_list"]))
            team_list.full_clean()
            team_list.save()

            for team_data in data["team_list"]:
                team = Team(
                    team_list=team_list,
                )
                for key, value in team_data.items():
                    setattr(team, key, value)

                team.full_clean()
                team.save()
            data.pop("team_list")

            # Create draw
            draw = Draw(user=user, player_list=player_list, team_list=team_list)
            for key, value in data.items():
                setattr(draw, key, value)

            draw.full_clean()
            draw.save()

            return Response(
                {"success": "List created"},
                status=status.HTTP_201_CREATED,
            )


class EditDrawAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        user = self.request.user
        data = self.request.data

        draw = Draw.objects.filter(id=data["id"], user=user).first()
        if draw:
            with transaction.atomic():
                data.pop("id")

                # Edit player list
                draw.player_list.players = len(data["player_list"])
                draw.player_list.full_clean()
                draw.player_list.save()

                Player.objects.filter(player_list=draw.player_list).delete()
                for player_data in data["player_list"]:
                    player = Player(
                        player_list=draw.player_list,
                    )
                    for key, value in player_data.items():
                        setattr(player, key, value)

                    player.full_clean()
                    player.save()
                data.pop("player_list")

                # Edit team list
                draw.team_list.teams = len(data["team_list"])
                draw.team_list.full_clean()
                draw.team_list.save()

                Team.objects.filter(team_list=draw.team_list).delete()
                for team_data in data["team_list"]:
                    team = Team(
                        team_list=draw.team_list,
                    )
                    for key, value in team_data.items():
                        setattr(team, key, value)

                    team.full_clean()
                    team.save()
                data.pop("team_list")

                # Edit draw
                for key, value in data.items():
                    setattr(draw, key, value)

                draw.full_clean()
                draw.save()

                return Response(
                    {"success": "List edited"},
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(
                {"error": "Draw not found"}, status=status.HTTP_404_NOT_FOUND
            )


class DeleteDrawAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, id, format=None):
        user = self.request.user

        draw = Draw.objects.filter(id=id).first()
        if draw:
            # By deleting player list, you delete draw. Because of on delete CASCADE
            draw.player_list.delete()
            return Response(
                {"success": "Draw deleted"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Draw not found"}, status=status.HTTP_404_NOT_FOUND
            )
