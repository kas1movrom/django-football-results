"""Views for main project."""

from django.shortcuts import render


def index(request):
    """/ path. Returns Hello, Forecasters."""
    return render(
        request,
        "index.html",
        context={
            "who": "Forecaster",
        },
    )
