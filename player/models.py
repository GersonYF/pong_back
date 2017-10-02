# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

GENDERS = (
    ('F', 'Feminine'),
    ('M', 'Masculine'),
)

class Player(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    picture = models.FileField(upload_to="pictures/", blank=True)
    gender = models.CharField(max_length=1, choices=GENDERS)
    birthday = models.DateField(blank=True)
    motto = models.CharField(max_length=120)

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name


class PlayerBoard(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name="board")
    points = models.IntegerField(default=0)
    win_count = models.IntegerField(default=0)
    lose_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.player.user.first_name + " " + self.player.user.last_name

    @receiver(post_save, sender=Player)
    def create_player_board(sender, instance, created, **kwargs):
        if created:
            PlayerBoard.objects.create(player=instance)

    @receiver(post_save, sender=User)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)
