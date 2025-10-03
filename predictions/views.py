"""init."""

from django.shortcuts import render

from .models import Game, NationalTeam


def games(request):
    """View for /predictions/games path."""
    sort_field = request.GET.get("sort")  # result, stadium, game_time
    desc = request.GET.get("desc")  # true or false
    owner_name = request.GET.get("name")  # Spain, England or Portugal

    ALLOWED_SORT_FIELDS = {"result", "stadium", "game_time"}

    games_list = Game.objects.select_related("stage").all()

    if owner_name:
        games_list = games_list.filter(owner__name=owner_name)

    if sort_field in ALLOWED_SORT_FIELDS:
        order_prefix = "-" if desc == "true" else ""
        games_list = games_list.order_by(f"{order_prefix}{sort_field}")

    all_teams = NationalTeam.objects.all().order_by("name")

    context = {
        "games_list": games_list,
        "all_teams": all_teams,
        "filters": {"sort": sort_field, "desc": desc, "name": owner_name},
    }

    return render(request, "predictions/games.html", context=context)


# Create your views here.
