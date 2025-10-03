"""init."""

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Forecast, Forecaster, Game, NationalTeam, Participation, Stage, Tournament


# TODO: добавить возможность импорта/эскпорта для всех моделей
class GameResource(resources.ModelResource):
    """Resource for game export and import."""

    class Meta:
        """Pointer to the model."""

        model = Game


# TODO: в list_filer можно добавить дополнительные поля (например для игры это может быть турнир)
# почему-ту не проходит фильтр

# TODO: изменить название столбцов в админ панели
# TODO: add ngettext


class ForecastInline(admin.TabularInline):
    """Inline."""

    model = Forecast


class GameInline(admin.TabularInline):
    """Inline."""

    model = Game


class GameOwnerInline(admin.StackedInline):
    """Inline."""

    model = Game
    fk_name = "owner"


class GameGuestInline(admin.StackedInline):
    """Inline."""

    model = Game
    fk_name = "guest"


class StageInline(admin.TabularInline):
    """Inline."""

    model = Stage


class NationalTeamInline(admin.TabularInline):
    """Inline."""

    model = Tournament.national_teams.through


class ParticipationInline(admin.TabularInline):
    """Inline."""

    model = Participation
    extra = 1


class NationalTeamAdmin(admin.ModelAdmin):
    """Admin model."""

    inlines = (GameOwnerInline, GameGuestInline)

    list_display = ("name", "mainland", "world_cup_count")
    list_filter = ("mainland", "world_cup_count")
    search_fields = ("name", "mainland")


class ForecasterAdmin(admin.ModelAdmin):
    """Admin model."""

    inlines = (ForecastInline, ParticipationInline)

    list_display = ("first_name", "last_name", "telegram", "birthday")


class TournamentAdmin(admin.ModelAdmin):
    """Admin model."""

    inlines = (StageInline, NationalTeamInline, ParticipationInline)
    exclude = ("national_teams",)

    list_display = ("place", "year", "active", "winner")
    list_filter = ("place", "winner")


class ForecastAdmin(admin.ModelAdmin):
    """Admin model."""

    actions = ("save_forecasts", "apply_forecasts")

    @admin.action(description="Mark selected forecasts as saved")
    def save_forecasts(self, request, queryset):
        """Set forecast status to saved."""
        queryset.update(status="SV")

    @admin.action(description="Mark selected forecasts as applied")
    def apply_forecasts(self, request, queryset):
        """Set forecast status to applied."""
        queryset.update(status="AP")

    # game__stage__tournament
    list_display = ("player", "game", "result", "game__result", "doubled", "status", "points", "game__stage")
    list_filter = ("player", "game", "doubled", "game__stage__st_type", "game__stage__tournament__place")
    search_fields = ("player__first_name", "player__last_name", "result", "game__result")


# TODO: спросить, как можно реализовать автоматическоедобавление очков при добавлении рез-та
class ParticipationAdmin(admin.ModelAdmin):
    """Admin model."""

    actions = ("calculate_points",)

    @admin.action(description="Calculate player points")  # TODO: добавить учет статуса прогноза и прочих статусов
    def calculate_points(self, request, queryset):
        """Calculate points for selected player and tournament."""
        for participation in queryset:
            participation.points = participation.count_points()
            participation.save()

    list_display = ("forecaster", "tournament", "player_points", "points")
    list_filter = ("forecaster", "tournament")
    search_fields = ("tournament__place", "tournament__year", "forecaster__first_name", "forecaster__last_name")


class GameAdmin(ImportExportModelAdmin):
    """Admin model."""

    resource_classes = (GameResource,)

    actions = ("playing_games", "finish_games")

    @admin.action(description="Mark selected games as playing")
    def playing_games(self, request, queryset):
        """Set games status to playing."""
        queryset.update(status="PL")

    @admin.action(description="Mark selected games as finished")
    def finish_games(self, request, queryset):
        """Set games status to finished."""
        queryset.update(status="FN")

    inlines = (ForecastInline,)

    list_display = (
        "owner",
        "guest",
        "result",
        "all_result",
        "stadium",
        "stage",
        "bucket_number",
        "game_time",
        "status",
    )

    list_filter = ("owner", "guest", "result", "stadium", "stage__tournament__place", "stage__tournament__year")

    search_fields = ("owner", "guest", "result", "stadium")


class StageAdmin(admin.ModelAdmin):
    """Admin model."""

    actions = ("open_stages", "start_stages", "close_stages")

    @admin.action(description="Mark selected stages as open")
    def open_stages(self, request, queryset):
        """Set selected stages status as opened."""
        queryset.update(status="OP")

    @admin.action(description="Mark selected stages as started")
    def start_stages(self, request, queryset):
        """Set selected stages status as started."""
        queryset.update(status="IP")

    @admin.action(description="Mark selected stages as closed")
    def close_stages(self, request, queryset):
        """Set selected stages status as closed."""
        queryset.update(status="CL")

    inlines = (GameInline,)

    list_display = ("tournament", "start_date", "finish_date", "st_type", "stage_number", "status")
    list_filter = ("tournament__place", "tournament__year", "st_type")
    search_fields = ("tournament__place", "tournament__year", "st_type")


admin.site.register(Forecaster, ForecasterAdmin)
admin.site.register(Forecast, ForecastAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(NationalTeam, NationalTeamAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(Participation, ParticipationAdmin)

# Register your models here.
