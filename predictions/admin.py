"""init."""

from django.contrib import admin

from .models import Forecast, Forecaster, Game, NationalTeam, Participation, Stage, Tournament

admin.site.register(Forecaster)
admin.site.register(Forecast)
admin.site.register(Tournament)
admin.site.register(NationalTeam)
admin.site.register(Game)
admin.site.register(Stage)
admin.site.register(Participation)

# Register your models here.
