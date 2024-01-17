from django.db import IntegrityError, transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from apps.team.api.serializers import TeamListSerializer, TeamSerializer
from apps.team.models import Team, TeamList, UserTeamList


class UserTeamListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = self.request.user

        user_team_lists = UserTeamList.objects.filter(user=user)
        if user_team_lists.exists():
            team_lists = [
                user_team_list.team_list for user_team_list in user_team_lists
            ]
            team_lists_serializer = TeamListSerializer(team_lists, many=True)

            return Response(
                {"team_lists": team_lists_serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Team lists not found"}, status=status.HTTP_404_NOT_FOUND
            )


class TeamListDetailAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id):
        user = self.request.user

        team_list = TeamList.objects.filter(id=id).first()
        if (
            team_list
            and UserTeamList.objects.filter(user=user, team_list=team_list).exists()
        ):
            result = {
                "id": team_list.id,
                "title": team_list.title,
            }

            teams = Team.objects.filter(team_list=team_list)
            teams_serializer = TeamSerializer(teams, many=True)

            result["teams"] = teams_serializer.data

            return Response(
                {"team_list": result},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Team list not found"}, status=status.HTTP_404_NOT_FOUND
            )


class CreateUserTeamListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = self.request.user

        data = self.request.data
        with transaction.atomic():
            team_list = TeamList(title=data["title"], teams=len(data["teams"]))
            team_list.full_clean()
            team_list.save()

            user_team_list = UserTeamList(user=user, team_list=team_list)
            user_team_list.full_clean()
            user_team_list.save()

            for team_data in data["teams"]:
                team = Team(
                    team_list=team_list,
                )
                for key, value in team_data.items():
                    setattr(team, key, value)

                team.full_clean()
                team.save()

            return Response(
                {"success": "List created"},
                status=status.HTTP_201_CREATED,
            )


class EditUserTeamListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, format=None):
        user = self.request.user
        data = self.request.data

        team_list = TeamList.objects.filter(id=data["id"]).first()
        if (
            team_list
            and UserTeamList.objects.filter(user=user, team_list=team_list).exists()
        ):
            with transaction.atomic():
                team_list.title = data["title"]
                team_list.teams = len(data["teams"])
                team_list.full_clean()
                team_list.save()

                Team.objects.filter(team_list=team_list).delete()

                for team_data in data["teams"]:
                    team = Team(
                        team_list=team_list,
                    )
                    for key, value in team_data.items():
                        setattr(team, key, value)

                    team.full_clean()
                    team.save()

                return Response(
                    {"success": "List edited"},
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(
                {"error": "Team list not found"}, status=status.HTTP_404_NOT_FOUND
            )


class DeleteUserTeamListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, id, format=None):
        user = self.request.user

        team_list = TeamList.objects.filter(id=id).first()
        if (
            team_list
            and UserTeamList.objects.filter(user=user, team_list=team_list).exists()
        ):
            team_list.delete()
            return Response(
                {"success": "List deleted"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Team list not found"}, status=status.HTTP_404_NOT_FOUND
            )
