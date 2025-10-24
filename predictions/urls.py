"""Urls."""

from django.urls import path

from . import views

app_name = "predictions"
urlpatterns = [
    path("forecasts/", views.my_forecasts, name="my-forecasts"),
    path("profile/", views.forecaster_profile, name="forecaster-profile"),
    path("games/", views.GameListView.as_view(), name="games"),
    path("game/<int:game_id>/", views.GameDetailView.as_view(), name="game-detail"),
    path("game/add/", views.GameCreateView.as_view(), name="add-game"),
    path("game/<int:game_id>/edit/", views.GameUpdateView.as_view(), name="edit-game"),
    path("game/<int:game_id>/delete/confirm/", views.GameDeleteView.as_view(), name="delete-game-confirm"),
    path("game/<int:game_id>/delete/", views.GameDeleteView.as_view(), name="delete-game"),
    path("forecast/add/", views.ForecastCreateView.as_view(), name="add-forecast"),
    path("forecast/<int:forecast_id>/edit/", views.ForecastUpdateView.as_view(), name="edit-forecast"),
    path(
        "forecast/<int:forecast_id>/delete/confirm/", views.ForecastDeleteView.as_view(), name="delete-forecast-confirm"
    ),
    path("forecast/<int:forecast_id>/delete/", views.ForecastDeleteView.as_view(), name="delete-forecast"),
    path("game/<int:game_id>/forecasts/", views.GameForecastsView.as_view(), name="game-forecasts"),
    path("game/<int:game_id>/forecast/<int:forecast_id>/", views.ForecastDetailView.as_view(), name="game-forecast"),
    path("national_teams/", views.NationalTeamListView.as_view(), name="national-teams"),
    path("national_team/<int:national_team_id>/", views.NationalTeamDetailView.as_view(), name="national-team-detail"),
    path("national_team/add/", views.NationalTeamCreateView.as_view(), name="add-national-team"),
    path(
        "national_team/<int:national_team_id>/edit/", views.NationalTeamUpdateView.as_view(), name="edit-national-team"
    ),
    path(
        "national_team/<int:national_team_id>/delete/confirm/",
        views.NationalTeamDeleteView.as_view(),
        name="delete-national-team-confirm",
    ),
    path(
        "national_team/<int:national_team_id>/delete/",
        views.NationalTeamDeleteView.as_view(),
        name="delete-national-team",
    ),
]
