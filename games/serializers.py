from rest_framework import serializers
from .models import Game, Score
from player.models import Player
from player.serializers import PlayerSerializer
from rest_framework import status
from rest_framework.response import Response

class ScoreSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)
    player_pk = serializers.IntegerField(write_only=True)

    class Meta:
        model = Score
        fields = ('player', 'points', 'player_pk')


class GameSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    date = serializers.DateTimeField(required=True)
    game_score = ScoreSerializer(many=True)
    owner = PlayerSerializer(read_only=True)
    owner_pk = serializers.IntegerField(write_only=True)

    class Meta:
        model = Game
        fields = ('id', 'date', 'owner')


    def updateBoardScore(self, game):
        scores = game.game_score.all()
        if scores.count() > 0:
            for score in scores:
                if score.player.user.pk == game.owner.user.pk:
                    player = score.player
                    player_score = score.points
                else:
                    rival = score.player
                    rival_score = score.points

            if player_score > rival_score:
                # Player Won - Rival Lose
                diff = player_score - rival_score
                player.board.win_count +=1
                rival.board.lose_count += 1

                if diff < 2:
                    player.board.points += 1
                else:
                    if player.board.points > rival.board.points:
                        # Player Stats better than rival
                        player.board.points += 2
                    else:
                        # Congrat and punish
                        player.board.points += 3
                        rival.board.points = 0 if (rival.board.points - 1) < 0 else rival.board.points - 1
            else:
                # Player Lose - Rival Won
                diff = rival_score - player_score
                rival.board.win_count += 1
                player.board.lose_count += 1

                if diff < 2:
                    rival.board.points += 1
                else:
                    if rival.board.points > player.board.points:
                        # Player Stats better than rival
                        rival.board.points += 2
                    else:
                        # Congrat and punish
                        rival.board.points += 3
                        player.board.points = 0 if (player.board.points - 1) < 0 else player.board.points - 1

            player.board.save()
            rival.board.save()

    def create(self, validated_data):
        owner_pk = validated_data.pop('owner_pk')
        owner = Player.objects.get(pk=owner_pk)
        game_score = validated_data.pop('game_score')
        game = Game.objects.create(owner=owner, **validated_data)
        for score in game_score:
            player = Player.objects.get(pk=score['player_pk'])
            Score.objects.create(game=game, player=player, points=score['points'])
        self.updateBoardScore(game)
        return game

    def update(self, instance, validated_data):
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance
