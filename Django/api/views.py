from api import serializers
from rest_framework import generics
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from recommendations.models import Rule, Code

# Create your views here.


class ListAllRules(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Rule.objects.all()
    serializer_class = serializers.RulesSerializer


class ListAllCodes(generics.ListAPIView):
    queryset = Code.objects.all()
    serializer_class = serializers.CodesSerializer

#TO DO: implement access permissions?

#BELOW EXAMPLE FILTERING
class ListPlayersInNhlTeamView(APIView):
    def get_object(self, pk):
        try:
            team = NhlTeam.objects.get(team_name=pk)
            players = NhlPlayers.objects.filter(team_name=pk)
            for player in players:
                if NhlSkaters.objects.filter(id=player.id).exists():
                    nhlskater = NhlSkaters.objects.get(id=player.id)
                    if nhlskater.center_flag:
                        player.position = "Center"
                    elif nhlskater.left_wing_flag:
                        player.position = "Left Wing"
                    elif nhlskater.right_wing_flag:
                        player.position = "Right Wing"
                    elif nhlskater.defencemen_flag:
                        player.position = "Defenceman"
                else:
                    player.position='Goalie'
                    
            return players
        except ObjectDoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None, **kwargs):
        queryset = self.get_object(pk)
        serializer = serializers.NhlPlayersSerializer(queryset, many=True)
        return Response(serializer.data)