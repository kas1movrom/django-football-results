"""Urls."""

from django.urls import path

from . import views

app_name = "predictions"
urlpatterns = [
    path(
        "tournament/<int:tournament_id>/participation/<int:participation_id>",
        views.ParticipationDetailView.as_view(),
        name="participation-detail",
    ),
    path(
        "tournament/<int:tournament_id>/participation/<int:participation_id>/edit/",
        views.ParticipationUpdateView.as_view(),
        name="edit-participation",
    ),
    path(
        "tournament/<int:tournament_id>/participation/<int:participation_id>/delete/",
        views.ParticipationDeleteView.as_view(),
        name="delete-participation",
    ),
    path(
        "tournament/<int:tournament_id>/participation/add",
        views.ParticipationCreateView.as_view(),
        name="add-participation",
    ),
    path("forecasts/", views.my_forecasts, name="my-forecasts"),
    path("profile/", views.forecaster_profile, name="forecaster-profile"),
    path("games/", views.GameListView.as_view(), name="games"),
    path("game/<int:game_id>/", views.GameDetailView.as_view(), name="game-detail"),
    path("game/add/", views.GameCreateView.as_view(), name="add-game"),
    path("game/<int:game_id>/edit/", views.GameUpdateView.as_view(), name="edit-game"),
    path("game/<int:game_id>/delete/", views.GameDeleteView.as_view(), name="delete-game"),
    path("forecast/add/", views.ForecastCreateView.as_view(), name="add-forecast"),
    path("forecast/<int:forecast_id>/edit/", views.ForecastUpdateView.as_view(), name="edit-forecast"),
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
        "national_team/<int:national_team_id>/delete/",
        views.NationalTeamDeleteView.as_view(),
        name="delete-national-team",
    ),
    path("stage/<int:stage_id>/", views.StageDetailView.as_view(), name="stage-detail"),
    path("tournament/<int:tournament_id>", views.TournamentDetailView.as_view(), name="tournament-detail"),
    path("tournament/<int:tournament_id>/edit", views.TournamentUpdateView.as_view(), name="edit-tournament"),
    path("tournament/<int:tournament_id>/delete", views.TournamentDeleteView.as_view(), name="delete-tournament"),
    path("tournament/add", views.TournamentCreateView.as_view(), name="add-tournament"),
    path("forecaster/<int:forecaster_id>", views.ForecasterDetailView.as_view(), name="forecaster-detail"),
    path("forecaster/add", views.ForecasterCreateView.as_view(), name="add-forecaster"),
    path("forecaster/<int:forecaster_id>/edit", views.ForecasterUpdateView.as_view(), name="edit-forecaster"),
    path("forecaster/<int:forecaster_id>/delete", views.ForecasterDeleteView.as_view(), name="delete-forecaster"),
    path("stage/<int:stage_id>/edit", views.StageUpdateView.as_view(), name="edit-stage"),
    path("stage/<int:stage_id>/delete", views.StageDeleteView.as_view(), name="delete-stage"),
    path("stage/add", views.StageCreateView.as_view(), name="add-stage"),
]
