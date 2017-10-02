from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from .models import Player, PlayerBoard

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
        }


class PlayerboardSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayerBoard
        fields = ('points', 'win_count', 'lose_count')

class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    board = PlayerboardSerializer(read_only=True)

    class Meta:
        model = Player
        fields = ('user','picture', 'gender', 'birthday', 'motto', 'board')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = User.objects.create_user(**user_data)
        user.set_password(password)
        user.save()
        player = Player.objects.create(user=user, **validated_data)
        return player

    def update(self, instance, validated_data):
        instance.gender = validated_data.get('gender', instance.gender)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.motto = validated_data.get('motto', instance.motto)
        instance.board = validated_data.get('board', instance.board)
        instance.save()
        return instance
