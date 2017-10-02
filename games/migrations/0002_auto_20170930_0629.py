# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-30 06:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('games', '0001_initial'),
        ('player', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_score', to='player.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='player_points',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_points', to='games.Score'),
        ),
        migrations.AddField(
            model_name='game',
            name='rival_points',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rival_points', to='games.Score'),
        ),
    ]