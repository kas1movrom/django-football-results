from rest_framework import serializers

from .models import Forecaster, NationalTeam


class ForecasterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Forecaster
        fields = ("first_name", "last_name", "mail")


class NationalTeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NationalTeam
        fields = ("name", "world_cup_count", "mainland", "main_color")
