"""forms."""

import typing

from django import forms

from .models import Forecast, Forecaster, Game, NationalTeam, Participation, Stage, Tournament


class ParticipationForm(forms.ModelForm):
    class Meta:
        model = Participation
        fields = ("tournament", "forecaster", "points")


class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ("st_type", "number", "tournament", "start_date", "finish_date")

        widgets: typing.ClassVar = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "finish_date": forms.DateInput(attrs={"type": "date"}),
        }


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ("active", "year", "place", "teams_count", "winner", "start_date", "finish_date")

        widgets: typing.ClassVar = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "finish_date": forms.DateInput(attrs={"type": "date"}),
        }


class ForecasterForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5, "placeholder": "Describe yourself..."}),
        required=False,
        label="Description",
    )

    class Meta:
        model = Forecaster

        fields = fields = ("first_name", "last_name", "telegram", "mail", "birthday", "bio")

        widgets: typing.ClassVar = {"birthday": forms.DateInput(attrs={"type": "date"})}


class ForecasterProfileForm(forms.ModelForm):
    # Поля из User
    username = forms.CharField(max_length=150, disabled=True, help_text="Имя пользователя нельзя изменить")
    email = forms.EmailField()
    bio = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5, "placeholder": "Describe yourself..."}),
        required=False,
        label="Description",
    )

    class Meta:
        model = Forecaster
        fields = ("first_name", "last_name", "telegram", "mail", "birthday", "bio")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["email"].initial = self.user.email
            self.fields["username"].initial = self.user.username

    def save(self, commit=True):
        forecaster = super().save(commit=False)
        if self.user:
            self.user.email = self.cleaned_data["email"]
            if commit:
                self.user.save()
        if commit:
            forecaster.save()
        return forecaster


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
