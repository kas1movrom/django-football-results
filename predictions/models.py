"""init."""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


# NOTE: can set ImageField instead of main_color use
class NationalTeam(models.Model):
    """Model for the national football team."""

    world_cup_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    name = models.CharField(max_length=20, unique=True)
    mainland = models.CharField(max_length=20)
    main_color = models.CharField(max_length=20)

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

    class Meta:  # noqa: D106
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(fields=["first_name", "last_name"], name="unique_fio")
        ]

    def __str__(self):
        """Returns first_name and last_name of the player."""
        return self.first_name + " " + self.last_name


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
        return self.place + " " + str(self.year)


# TODO: add register time (dig)
class Participation(models.Model):
    """Model for ManyToMany relation between Tournament and Forecaster."""

    forecaster = models.ForeignKey(Forecaster, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    register_time = models.DateTimeField(auto_now_add=True)

    class Meta:  # noqa: D106
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(fields=["forecaster", "tournament"], name="unique_forecaster_tournament")
        ]

    def __str__(self):
        """Returns Tournament (Player): points."""
        return f"{self.tournament} ({self.forecaster}): {self.points}"


# TODO: add start and end date of the stage (dig)
# TODO: fix unique field in the diagram (dig)
class Stage(models.Model):
    """Model for stages of each tournament."""

    class StageStatus(models.TextChoices):  # noqa: D106
        OPEN = "OP", _("Open")
        IN_PROGRESS = "IP", _("In Progress")
        CLOSED = "CL", _("Closed")

    class StageType(models.TextChoices):  # noqa: D106
        GROUP = "GR", _("Group")
        PLAY_OFF = "PL", _("Play-Off")

    status = models.CharField(max_length=2, choices=StageStatus, default=StageStatus.CLOSED)
    st_type = models.CharField(max_length=2, choices=StageType)
    number = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(64)])
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    start_date = models.DateField()
    finish_date = models.DateField()

    class Meta:  # noqa: D106
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(fields=["st_type", "number", "tournament"], name="unique_type_number_tournament")
        ]

    def __str__(self):
        """Returns 1/2 : Play-off (Russia 2018)."""
        stg = f"Tour {self.number}" if self.st_type == "GR" else ("Final" if self.number == 1 else f"1/{self.number}")

        return f"{stg} : {self.get_st_type_display()} ({self.tournament})"


# TODO: fix ERD diagram (dig)
class Game(models.Model):
    """Model for a game in the tournament."""

    class GameStatus(models.TextChoices):  # noqa: D106
        NOT_STARTED = "NS", _("Not Started")
        PLAYING = "PL", _("Playing")
        FINISHED = "FN", _("Finished")

    stadium = models.CharField(max_length=20)
    game_time = models.DateTimeField()
    number = models.CharField(max_length=2)  # Number of a group or number of a game in the play-off

    status = models.CharField(max_length=2, choices=GameStatus, default=GameStatus.NOT_STARTED)

    # NOTE: can add regex validation
    result = models.CharField(max_length=5, blank=True)
    all_result = models.CharField(max_length=12, blank=True)

    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    owner = models.ForeignKey(NationalTeam, on_delete=models.CASCADE, related_name="home_games")
    guest = models.ForeignKey(NationalTeam, on_delete=models.CASCADE, related_name="away_games")

    def __str__(self):
        """Returns home - away (tournament)."""
        return f"{self.owner} - {self.guest} ({self.stage.tournament})"


class Forecast(models.Model):
    """Model for a forecast on the match from forecaster."""

    class ForecastStatus(models.TextChoices):  # noqa: D106
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
