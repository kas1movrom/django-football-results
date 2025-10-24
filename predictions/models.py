"""init."""

import functools

from django.contrib import admin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


# TODO: добавить imagefield (lecture-4)
# TODO: добавить уникальность на некоторые столбцы (lecture-4)
# TODO: добавить verbose name (также добавить в Meta) (lecture-4)
def validate_game_result(result):
    """Validates result of the game."""
    if "-" in result:
        goals = result.split("-")

        if len(goals) == 2 and goals[0].isdigit() and goals[-1].isdigit():
            return

    if result:
        raise ValidationError(_("%(result)s is not a valid result"), params={"result": result})


# Create your models here.

# TODO: добавить в приложение учёт статусов всех сущностей


# NOTE: can set ImageField instead of main_color use - сделать это
class NationalTeam(models.Model):
    """Model for the national football team."""

    world_cup_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    name = models.CharField(max_length=20, unique=True)
    mainland = models.CharField(max_length=20)
    main_color = models.CharField(max_length=20)
    flag = models.ImageField(upload_to="flags/", blank=True, null=True)

    def __str__(self):
        """Returns name of the country."""
        return self.name


# TODO: add uniqieness on first and last names (dig)
class Forecaster(models.Model):
    """Model for forecaster person."""

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    # TODO: regexp validation
    telegram = models.CharField(max_length=50)
    mail = models.EmailField()
    admin = models.BooleanField(default=False)
    birthday = models.DateField()

    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(fields=["first_name", "last_name"], name="unique_fio")
        ]

    def __str__(self):
        """Returns first_name and last_name of the player."""
        return f"{self.first_name} {self.last_name}"


# TODO: add start and end date of the tournament (dig)
class Tournament(models.Model):
    """Model for international football tournament."""

    active = models.BooleanField(default=False)
    year = models.IntegerField(unique=True, validators=[MinValueValidator(2000)])
    place = models.CharField(max_length=30)
    teams_count = models.IntegerField(validators=[MinValueValidator(16)])
    winner = models.CharField(max_length=20, blank=True)
    start_date = models.DateField()
    finish_date = models.DateField()

    national_teams = models.ManyToManyField(NationalTeam)

    forecasters = models.ManyToManyField(Forecaster, through="Participation")

    def __str__(self):
        """Returns a place and a year for tournament."""
        return f"{self.place} {self.year}"


# TODO: add register time (dig)
class Participation(models.Model):
    """Model for ManyToMany relation between Tournament and Forecaster."""

    forecaster = models.ForeignKey(Forecaster, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    register_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(fields=["forecaster", "tournament"], name="unique_forecaster_tournament")
        ]

    def __str__(self):
        """Returns Tournament (Player): points."""
        return f"{self.tournament} ({self.forecaster}): {self.points}"

    def count_points(self):
        """Returns player points on the tournament."""
        return functools.reduce(
            lambda x, y: x + y.doubled_points(),
            Forecast.objects.filter(player=self.forecaster).filter(game__stage__tournament=self.tournament),
            0,
        )

    @admin.display(description="Points")
    def player_points(self):
        """Returns points for admin panel."""
        return self.count_points()


# TODO: fix unique field in the diagram (dig)
class Stage(models.Model):
    """Model for stages of each tournament."""

    class StageStatus(models.TextChoices):
        OPEN = "OP", _("Open")
        IN_PROGRESS = "IP", _("In Progress")
        CLOSED = "CL", _("Closed")

    class StageType(models.TextChoices):
        GROUP = "GR", _("Group")
        PLAY_OFF = "PL", _("Play-Off")

    status = models.CharField(max_length=2, choices=StageStatus, default=StageStatus.CLOSED)
    st_type = models.CharField(max_length=2, choices=StageType)
    number = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(64)])
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    start_date = models.DateField()
    finish_date = models.DateField()

    class Meta:
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(fields=["st_type", "number", "tournament"], name="unique_type_number_tournament")
        ]

    def __str__(self):
        """Returns 1/2 : Play-off (Russia 2018)."""
        return f"{self.get_pretty_number()} : {self.get_st_type_display()} ({self.tournament})"

    def get_pretty_number(self):
        """Returns pretty stage number."""
        if self.st_type == "GR":
            return f"Tour #{self.number}"

        if self.number == 1:
            return "Final"

        return f"1/{self.number}"

    @admin.display(description="Stage number")
    def stage_number(self):
        """Returns pretty stage number for admin panel."""
        return self.get_pretty_number()


# TODO: fix ERD diagram (dig)
class Game(models.Model):
    """Model for a game in the tournament."""

    class GameStatus(models.TextChoices):
        NOT_STARTED = "NS", _("Not Started")
        PLAYING = "PL", _("Playing")
        FINISHED = "FN", _("Finished")

    stadium = models.CharField(max_length=20)
    game_time = models.DateTimeField()
    number = models.CharField(max_length=2)  # Number of a group or number of a game in the play-off

    status = models.CharField(max_length=2, choices=GameStatus, default=GameStatus.NOT_STARTED)

    # NOTE: can add regex validation
    result = models.CharField(max_length=5, blank=True, validators=[validate_game_result])
    all_result = models.CharField(max_length=12, blank=True)  # TODO: add custom validator

    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    owner = models.ForeignKey(NationalTeam, on_delete=models.CASCADE, related_name="home_games")
    guest = models.ForeignKey(NationalTeam, on_delete=models.CASCADE, related_name="away_games")

    def __str__(self):
        """Returns home - away (tournament)."""
        return f"{self.owner} - {self.guest} ({self.stage.tournament})"

    @staticmethod
    def get_pretty_number(num):
        """Returns pretty number of Group or game in the play-off."""
        if num.isalpha():
            return f"Group {num}"

        return num

    @admin.display(description="Bucket number")
    def bucket_number(self):
        """Pretty method for admin panel."""
        return Game.get_pretty_number(self.number)


# TODO: поменять название поля result (если это возможно)
# TODO: почему прогноз не содержит количество очков....
class Forecast(models.Model):
    """Model for a forecast on the match from forecaster."""

    class ForecastStatus(models.TextChoices):
        EMPTY = "EM", _("Empty")
        SAVED = "SV", _("Saved")
        APPLIED = "AP", _("Applied")

    doubled = models.BooleanField(default=False)
    result = models.CharField(max_length=5, blank=True)
    register_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=ForecastStatus, default=ForecastStatus.EMPTY)

    player = models.ForeignKey(Forecaster, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        """Returns player data -- game data and predict."""
        return f"[{self.player} -- {self.game}] : {self.result}"

    @staticmethod
    def __same_winner(owner, guest, predict_owner, predict_guest):
        diff = owner - guest
        predict_diff = predict_owner - predict_guest

        return diff * predict_diff > 0

    def gm_result(self):
        """Returns result of the game."""
        return self.game.result

    def doubled_points(self):
        """Returns doubled points if forecast was doubled."""
        bp = self.base_points()

        return bp * 2 if self.doubled else bp

    def base_points(self):
        """Returns points for the forecast."""
        own, gst = [int(goals) for goals in self.gm_result().split("-")]
        p_own, p_gst = [int(goals) for goals in self.result.split("-")]

        if own == p_own and gst == p_gst:
            return 3

        if own - gst == p_own - p_gst:
            return 2

        if Forecast.__same_winner(own, gst, p_own, p_gst):
            return 1

        return 0

    @admin.display(description="Points")
    def points(self):
        """Returns points for admin."""
        return self.doubled_points()
