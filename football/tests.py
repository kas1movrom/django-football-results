from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from predictions.models import Forecaster, Tournament
from predictions.tests import create_tournament


def create_forecaster():
    return Forecaster.objects.create(first_name="Roman", last_name="Kasimov", mail="romkasrm11832@gmail.com")


def create_user():
    return User.objects.create_user(username="name", password="rfcbvjdh0vfy")


class FootballIndexViewTests(TestCase):
    def test_move_to_sign_up(self):
        response = self.client.get(reverse("index"))
        assert response.status_code == 302

    def test_football_main_page(self):
        create_user()
        create_forecaster()
        create_tournament()

        self.client.login(username="name", password="rfcbvjdh0vfy")
        response = self.client.get(reverse("index"))

        assert response.status_code == 200
        self.assertQuerySetEqual(response.context["closed_tournaments"], Tournament.closed.all())

    def test_incorrect_way(self):
        response = self.client.get("idx")
        assert response.status_code == 404
