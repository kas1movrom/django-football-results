"""init."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import (
    ForecasterForm,
    ForecasterProfileForm,
    ForecastForm,
    GameForm,
    NationalTeamForm,
    ParticipationForm,
    StageForm,
    TournamentForm,
)
from .models import Forecast, Forecaster, Game, NationalTeam, Participation, Stage, Tournament


class ForecasterDetailView(DetailView):
    model = Forecaster
    template_name = "predictions/forecaster.html"
    context_object_name = "forecaster"
    pk_url_kwarg = "forecaster_id"


# TODO: изменить GameDetailView, чтобы отображалсь ссылка обратно на stage
# TODO: сделать ссылку на добавление стейджа, принадлежащего турниру
class TournamentDetailView(DetailView):
    model = Tournament
    template_name = "predictions/tournament.html"
    context_object_name = "tournament"
    pk_url_kwarg = "tournament_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stages_list"] = self.object.stage_set.all()
        context["participations"] = self.object.participation_set.select_related("forecaster").all()
        return context


class ParticipationDetailView(DetailView):
    model = Participation
    template_name = "predictions/participation.html"
    context_object_name = "participation"
    pk_url_kwarg = "participation_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tournament"] = Tournament.objects.get(id=self.kwargs.get("tournament_id"))
        return context


class StageDetailView(DetailView):
    model = Stage
    template_name = "predictions/stage.html"
    context_object_name = "stage"
    pk_url_kwarg = "stage_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["games_list"] = self.object.game_set.select_related("owner").select_related("guest").all()
        return context


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


class TournamentCreateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, CreateView):
    model = Tournament
    form_class = TournamentForm
    template_name = "predictions/add_tournament.html"
    success_message = "Турнир успешно создан!"

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse("predictions:tournament-detail", kwargs={"tournament_id": self.object.pk})


class ParticipationCreateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, CreateView):
    model = Participation
    form_class = ParticipationForm
    template_name = "predictions/add_participation.html"
    success_message = "Участие успешно создано!"

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tournament"] = self.get_tournament()
        return context

    def get_tournament_id(self):
        return self.kwargs.get("tournament_id")

    def get_tournament(self):
        return Tournament.objects.get(id=self.get_tournament_id())

    def get_success_url(self):
        return reverse(
            "predictions:participation-detail",
            kwargs={"participation_id": self.object.pk, "tournament_id": self.get_tournament_id()},
        )


class ForecasterCreateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, CreateView):
    model = Forecaster
    form_class = ForecasterForm
    template_name = "predictions/add_forecaster.html"
    success_message = "Прогнозист успешно создан!"

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse("predictions:forecaster-detail", kwargs={"forecaster_id": self.object.pk})


class StageCreateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, CreateView):
    model = Stage
    form_class = StageForm
    template_name = "predictions/add_stage.html"
    success_message = "Стейдж успешно создан!"

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse("predictions:stage-detail", kwargs={"stage_id": self.object.pk})


class GameCreateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, CreateView):
    model = Game
    form_class = GameForm
    template_name = "predictions/add_game.html"
    success_message = "Матч успешно создан!"

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse("predictions:game-detail", kwargs={"game_id": self.object.pk})


class TournamentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Tournament
    form_class = TournamentForm
    template_name = "predictions/edit_tournament.html"
    pk_url_kwarg = "tournament_id"
    success_message = "Турнир успешно обновлен!"

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse("predictions:tournament-detail", kwargs={"tournament_id": self.object.pk})


class ParticipationUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Participation
    form_class = ParticipationForm
    template_name = "predictions/edit_participation.html"
    pk_url_kwarg = "participation_id"
    success_message = "Участие успешно обновлено!"

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tournament"] = self.get_tournament()
        return context

    def get_tournament_id(self):
        return self.kwargs.get("tournament_id")

    def get_tournament(self):
        return Tournament.objects.get(id=self.get_tournament_id())

    def get_success_url(self):
        return reverse(
            "predictions:participation-detail",
            kwargs={"participation_id": self.object.pk, "tournament_id": self.get_tournament_id()},
        )


class StageUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Stage
    form_class = StageForm
    template_name = "predictions/edit_stage.html"
    pk_url_kwarg = "stage_id"
    success_message = "Стейдж успешно обновлен!"

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse("predictions:stage-detail", kwargs={"stage_id": self.object.pk})


class ForecasterUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Forecaster
    form_class = ForecasterForm
    template_name = "predictions/edit_forecaster.html"
    pk_url_kwarg = "forecaster_id"
    success_message = "Прогнозист успешно обновлен!"

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse("predictions:forecaster-detail", kwargs={"forecaster_id": self.object.pk})


class GameUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Game
    form_class = GameForm
    template_name = "predictions/edit_game.html"
    pk_url_kwarg = "game_id"
    success_message = "Матч успешно обновлён!"

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse("predictions:game-detail", kwargs={"game_id": self.object.pk})


class TournamentDeleteView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Tournament
    template_name = "predictions/delete_tournament_confirm.html"
    pk_url_kwarg = "tournament_id"
    success_message = "Турнир удалён."
    success_url = reverse_lazy("index")

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class ParticipationDeleteView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Participation
    template_name = "predictions/delete_participation_confirm.html"
    pk_url_kwarg = "participation_id"
    success_message = "Участие удалено"
    success_url = reverse_lazy("index")

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tournament"] = self.get_tournament()
        return context

    def get_tournament_id(self):
        return self.kwargs.get("tournament_id")

    def get_tournament(self):
        return Tournament.objects.get(id=self.get_tournament_id())

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class StageDeleteView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Stage
    template_name = "predictions/delete_stage_confirm.html"
    pk_url_kwarg = "stage_id"
    success_message = "Стейдж успешно удален!"
    success_url = reverse_lazy("index")

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# TODO: реализовать логику вывода последних n прогнозов (для этого они должны быть в статусе applied)
class ForecasterDeleteView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Forecaster
    template_name = "predictions/delete_forecaster_confirm.html"
    pk_url_kwarg = "forecaster_id"
    success_message = "Прогнозист успешно удалён!"
    success_url = reverse_lazy("index")

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class GameDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Game
    template_name = "predictions/delete_game_confirm.html"
    pk_url_kwarg = "game_id"
    success_message = "Матч удалён."
    success_url = reverse_lazy("predictions:games")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class ForecastCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Forecast
    form_class = ForecastForm
    template_name = "predictions/add_forecast.html"
    success_message = "Прогноз успешно сохранён!"

    def get_success_url(self):
        return reverse("predictions:game-forecasts", kwargs={"game_id": self.object.game.pk})


class ForecastUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Forecast
    form_class = ForecastForm
    template_name = "predictions/edit_forecast.html"
    pk_url_kwarg = "forecast_id"
    success_message = "Прогноз обновлён!"

    def get_object(self, queryset=None):
        forecast = super().get_object(queryset)
        if forecast.player.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("Вы не можете редактировать чужие прогнозы.")

        return forecast

    def get_success_url(self):
        return reverse(
            "predictions:game-forecast", kwargs={"game_id": self.object.game.pk, "forecast_id": self.object.pk}
        )


class ForecastDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Forecast
    template_name = "predictions/delete_forecast_confirm.html"
    pk_url_kwarg = "forecast_id"
    success_message = "Прогноз удалён."

    def get_success_url(self):
        return reverse("predictions:game-forecasts", kwargs={"game_id": self.object.game.pk})

    def get_object(self, queryset=None):
        forecast = super().get_object(queryset)
        if forecast.player.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("Вы не можете удалять чужие прогнозы.")

        return forecast

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


class NationalTeamListView(ListView):
    model = NationalTeam
    template_name = "predictions/national_teams.html"
    context_object_name = "national_teams_list"
    paginate_by = 5


class NationalTeamCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = NationalTeam
    form_class = NationalTeamForm
    template_name = "predictions/add_national_team.html"
    success_message = "Сборная успешно создана!"

    def get_success_url(self):
        return reverse("predictions:national-team-detail", kwargs={"national_team_id": self.object.pk})


class NationalTeamUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = NationalTeam
    form_class = NationalTeamForm
    template_name = "predictions/edit_national_team.html"
    pk_url_kwarg = "national_team_id"
    success_message = "Сборная успешно обновлена!"
    context_object_name = "national_team"

    def get_success_url(self):
        return reverse("predictions:national-team-detail", kwargs={"national_team_id": self.object.pk})


class NationalTeamDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = NationalTeam
    template_name = "predictions/delete_national_team_confirm.html"
    pk_url_kwarg = "national_team_id"
    success_message = "Сборная удалена."
    success_url = reverse_lazy("predictions:national-teams")
    context_object_name = "national_team"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


@login_required
def my_forecasts(request):
    forecaster = Forecaster.objects.get(user=request.user)
    return render(request, "predictions/my_forecasts.html", context={"forecasts": forecaster.forecast_set.all()})


# TODO: при изменении почты user-a не меняется почта прогнозиста
# TODO: здесь получим ошибку сразу при регистрации (т.к пользователь не привяжется к прогнозисту => надо фиксить)
@login_required
def forecaster_profile(request):
    # Получаем или создаём Forecaster для текущего пользователя не создаём
    forecaster = Forecaster.objects.get(user=request.user)

    if request.method == "POST":
        form = ForecasterProfileForm(request.POST, instance=forecaster, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваш профиль успешно обновлён!")
            return redirect("predictions:forecaster-profile")
    else:
        form = ForecasterProfileForm(instance=forecaster, user=request.user)

    return render(request, "predictions/forecaster_profile.html", {"form": form, "forecaster": forecaster})
