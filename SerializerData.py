from games.serializers import GameSerializer
from player.serializers import PlayerSerializer

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from player.models import Player

serializer = PlayerSerializer(Player.objects.all(), many=True)
content = JSONRenderer().render(serializer.data)
content
