"""init."""

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ForecastForm, GameForm, NationalTeamForm
from .models import Forecast, Game, NationalTeam


class GameListView(ListView):
    model = Game
    template_name = "predictions/games.html"
    context_object_name = "games_list"
    paginate_by = None

    def get_queryset(self):
        queryset = Game.objects.select_related("stage", "owner", "guest").prefetch_related("forecast_set")
        search_name = self.request.GET.get("name")
        if search_name:
            queryset = queryset.filter(Q(owner__name__icontains=search_name) | Q(guest__name__icontains=search_name))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_field = self.request.GET.get("sort")
        desc = self.request.GET.get("desc")
        search_name = self.request.GET.get("name")

        # Применяем сортировку
        allowed_sort_fields = {"result", "stadium", "game_time"}
        if sort_field in allowed_sort_fields:
            order_prefix = "-" if desc == "true" else ""
            context["games_list"] = context["games_list"].order_by(f"{order_prefix}{sort_field}")

        context["filters"] = {
            "sort": sort_field,
            "desc": desc,
            "name": search_name,
        }
        return context


class GameDetailView(DetailView):
    model = Game
    template_name = "predictions/game.html"
    context_object_name = "game"
    pk_url_kwarg = "game_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forecasts"] = self.object.forecast_set.select_related("player").all()
        return context


class GameCreateView(SuccessMessageMixin, CreateView):
    model = Game
    form_class = GameForm
    template_name = "predictions/add_game.html"
    success_message = "Матч %(stadium)s успешно создан!"

    def get_success_url(self):
        return reverse("predictions:game-detail", kwargs={"game_id": self.object.pk})


class GameUpdateView(SuccessMessageMixin, UpdateView):
    model = Game
    form_class = GameForm
    template_name = "predictions/edit_game.html"
    pk_url_kwarg = "game_id"
    success_message = "Матч успешно обновлён!"

    def get_success_url(self):
        return reverse("predictions:game-detail", kwargs={"game_id": self.object.pk})


class GameDeleteView(SuccessMessageMixin, DeleteView):
    model = Game
    template_name = "predictions/delete_game_confirm.html"
    pk_url_kwarg = "game_id"
    success_message = "Матч удалён."
    success_url = reverse_lazy("predictions:games")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class ForecastCreateView(SuccessMessageMixin, CreateView):
    model = Forecast
    form_class = ForecastForm
    template_name = "predictions/add_forecast.html"
    success_message = "Прогноз успешно сохранён!"

    def get_success_url(self):
        return reverse("predictions:game-forecasts", kwargs={"game_id": self.object.game.pk})


class ForecastUpdateView(SuccessMessageMixin, UpdateView):
    model = Forecast
    form_class = ForecastForm
    template_name = "predictions/edit_forecast.html"
    pk_url_kwarg = "forecast_id"
    success_message = "Прогноз обновлён!"

    def get_success_url(self):
        return reverse(
            "predictions:game-forecast", kwargs={"game_id": self.object.game.pk, "forecast_id": self.object.pk}
        )


class ForecastDeleteView(SuccessMessageMixin, DeleteView):
    model = Forecast
    template_name = "predictions/delete_forecast_confirm.html"
    pk_url_kwarg = "forecast_id"
    success_message = "Прогноз удалён."

    def get_success_url(self):
        return reverse("predictions:game-forecasts", kwargs={"game_id": self.object.game.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class GameForecastsView(DetailView):
    model = Game
    template_name = "predictions/forecasts.html"
    context_object_name = "game"
    pk_url_kwarg = "game_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forecasts"] = self.object.forecast_set.select_related("player").all()
        return context


class ForecastDetailView(DetailView):
    model = Forecast
    template_name = "predictions/forecast.html"
    context_object_name = "forecast"
    pk_url_kwarg = "forecast_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["game"] = self.object.game
        return context


class NationalTeamDetailView(DetailView):
    model = NationalTeam
    template_name = "predictions/national_team.html"
    context_object_name = "national_team"
    pk_url_kwarg = "national_team_id"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class NationalTeamListView(ListView):
    model = NationalTeam
    template_name = "predictions/national_teams.html"
    context_object_name = "national_teams_list"
    paginate_by = None

    def get_queryset(self):
        return NationalTeam.objects.all()

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class NationalTeamCreateView(SuccessMessageMixin, CreateView):
    model = NationalTeam
    form_class = NationalTeamForm
    template_name = "predictions/add_national_team.html"
    success_message = "Сборная успешно создана!"

    def get_success_url(self):
        return reverse("predictions:national-team-detail", kwargs={"national_team_id": self.object.pk})


class NationalTeamUpdateView(SuccessMessageMixin, UpdateView):
    model = NationalTeam
    form_class = NationalTeamForm
    template_name = "predictions/edit_national_team.html"
    pk_url_kwarg = "national_team_id"
    success_message = "Сборная успешно обновлена!"
    context_object_name = "national_team"

    def get_success_url(self):
        return reverse("predictions:national-team-detail", kwargs={"national_team_id": self.object.pk})


class NationalTeamDeleteView(SuccessMessageMixin, DeleteView):
    model = NationalTeam
    template_name = "predictions/delete_national_team_confirm.html"
    pk_url_kwarg = "national_team_id"
    success_message = "Сборная удалена."
    success_url = reverse_lazy("predictions:national-teams")
    context_object_name = "national_team"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
