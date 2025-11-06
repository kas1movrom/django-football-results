"""init."""

from datetime import date

from django.test import TestCase

from .models import NationalTeam, Tournament


def create_tournament(active=False):
    return Tournament.objects.create(
        active=active,
        year=2000,
        place="Somewhere",
        teams_count=20,
        start_date=date(2021, 7, 7),
        finish_date=date(2022, 7, 7),
    )


class NationalTeamModelTests(TestCase):
    def test_create_national_team_object(self):
        WORLD_CUP_COUNT = 3
        some_team = NationalTeam(world_cup_count=WORLD_CUP_COUNT, name="SomeTeam", mainland="Asia", main_color="Green")

        assert some_team.world_cup_count is WORLD_CUP_COUNT
        assert str(some_team) is some_team.name


class TournamentModelTests(TestCase):
    def test_closed_manager(self):
        create_tournament()

        assert Tournament.activated.all().count() == 0
        assert Tournament.closed.all().count() == 1
        assert Tournament.objects.all().count() == 1

    def test_active_manager(self):
        create_tournament(True)

        assert Tournament.activated.all().count() == 1
        assert Tournament.closed.all().count() == 0
        assert Tournament.objects.all().count() == 1

    def test_create_tournament_object(self):
        tourn = create_tournament(True)

        assert tourn.active is True


# Create your tests here.
