"""forms."""

import typing

from django import forms

from .models import Forecast, Game, NationalTeam


class GameForm(forms.ModelForm):
    """Form for Game Model."""

    class Meta:
        """Meta."""

        model = Game
        fields = (
            "stadium",
            "game_time",
            "number",
            "status",
            "result",
            "all_result",
            "stage",
            "owner",
            "guest",
        )
        widgets: typing.ClassVar = {
            "game_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class ForecastForm(forms.ModelForm):
    """Form for Forecast Model."""

    class Meta:
        """Meta."""

        model = Forecast
        fields = (
            "player",
            "game",
            "result",
            "doubled",
            "status",
        )
        widgets: typing.ClassVar = {
            "register_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class NationalTeamForm(forms.ModelForm):
    class Meta:
        """Meta."""

        model = NationalTeam

        fields = ("world_cup_count", "name", "mainland", "main_color", "flag")
        widgets: typing.ClassVar = {
            "flag": forms.FileInput(attrs={"accept": "image/*"}),
        }
