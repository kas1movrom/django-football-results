"""init."""

from django.apps import AppConfig


class PredictionsConfig(AppConfig):
    """init."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "predictions"

    def ready(self):
        import predictions.signals  # noqa: F401
