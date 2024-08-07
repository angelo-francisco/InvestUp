from . import forms
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages


def _signup(request):
    if request.user.is_authenticated:
        return redirect(reverse("showCompany"))

    form = forms.SignupForm()

    if request.method == "POST":
        form = forms.SignupForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Signup done successfully")
            return redirect(reverse("login"))

    context = {"form": form}
    return render(request, "registration/signup.html", context=context)


def _login(request):
    if request.user.is_authenticated:
        return redirect(reverse("showCompany"))

    form = forms.LoginForm()

    if request.method == "POST":
        form = forms.LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(request, "Login done successfully")
            return redirect(reverse("showCompany"))

    context = {"form": form}
    return render(request, "registration/login.html", context=context)


@login_required()
def _logout(request):
    logout(request)
    return redirect(reverse("login"))
