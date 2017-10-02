from django.conf.urls import url
from player import views

urlpatterns = [
    url(r'^players/$', views.player_list),
    url(r'^players/(?P<pk>[0-9]+)/$', views.player_detail),
    url(r'^players/detail/$', views.token_player),
    url(r'^players/games/$', views.player_games),
]
