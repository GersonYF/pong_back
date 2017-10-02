# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Player
from games.models import Game
from .serializers import PlayerSerializer
from games.serializers import GameSerializer

@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def player_list(request):

    if request.method == 'GET':
        players = Player.objects.all().order_by('-board__points')
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def player_detail(request, pk):

    try:
        player = Player.objects.get(pk=pk)
    except Player.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlayerSerializer(player)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PlayerSerializer(player, data=request.data)
        print serializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        player.delete()
        return Response(status=status.HTTP_204_NOT_CONTENT)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def token_player(request):
    if request.method == 'GET':
        player = Player.objects.get(user=request.user)
        serializer = PlayerSerializer(player)
        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def player_games(request):
    if request.method == 'GET':
        player = Player.objects.get(user=request.user)
        games = Game.objects.filter(game_score__player__user__pk=player.user.pk)
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
