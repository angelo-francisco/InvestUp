from . import forms
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout


def _signup(request):
    if request.user.is_authenticated:
        return redirect(reverse("addCompany"))

    form = forms.SignupForm()

    if request.method == "POST":
        form = forms.SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse("login"))

    context = {"form": form}
    return render(request, "registration/signup.html", context=context)


def _login(request):
    if request.user.is_authenticated:
        return redirect(reverse("addCompany"))

    form = forms.LoginForm()

    if request.method == "POST":
        form = forms.LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect(reverse("addCompany"))

    context = {"form": form}
    return render(request, "registration/login.html", context=context)


@login_required()
def _logout(request):
    logout(request)
    return redirect(reverse("login"))
