"""Views for main project."""

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from predictions.models import Forecaster, Tournament

from .forms import LoginForm, SignUpForm


# TODO: добавить logout
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем нового пользователя
            login(request, user)  # Выполняем вход
            messages.success(request, "Вы успешно зарегестрировались!")
            return redirect("index")  # Перенаправляем на главную страницу
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)  # Проверяем учетные данные
        if user is not None:
            login(request, user)  # Выполняем вход
            messages.success(request, "Вы успешно вошли в систему!")
            return redirect("index")  # Перенаправляем на главную страницу
    return render(request, "login.html", {"form": form})


@login_required
def index(request):
    """/ path. Returns Hello, Forecasters."""
    active_tournaments = Tournament.activated.all()
    closed_tournaments = Tournament.closed.all()
    forecasters = Forecaster.objects.all()
    return render(
        request,
        "index.html",
        context={
            "who": "Forecaster",
            "forecasters": forecasters,
            "closed_tournaments": closed_tournaments,
            "active_tournaments": active_tournaments,
        },
    )
