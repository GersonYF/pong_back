# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from player.models import Player

class Game(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __unicode__(self):
        return self.owner.user.first_name + " " + self.owner.user.last_name

class Score(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='game_score'
    )
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='player_score'
    )
    points = models.IntegerField(default=0)

    def __unicode__(self):
        return self.player.user.first_name + " " + self.player.user.last_name
