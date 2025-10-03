"""Urls for predictions app."""

from django.urls import path

from . import views

urlpatterns = [path("games/", views.games, name="games")]
