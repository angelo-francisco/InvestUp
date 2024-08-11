from . import forms
from companies.models import Company, Notifications
from investors.models import InvestmentProposal

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from secrets import compare_digest

force_text = force_str


@login_required
def change_password(request): ...


@login_required
def reseting_password(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

    if not user and not default_token_generator.check_token(user, token):
        messages.warning(request, 'Your token is invalid(maybe it expired)')
        return redirect(reverse("profile", args=[user.username]))
    
    if request.method == "POST":
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not compare_digest(str(password1).encode(), str(password2).encode()):
            messages.warning(request, "The passoword isn't equal")
            return redirect(reverse('reseting_password', kwargs={'uidb64': uidb64, 'token': token}))
        
        user.set_password(password1)
        user.save()

        messages.success(request, 'Password reseted successfuly')
        return redirect(reverse("profile", args=[user.username]))
    return render(request, 'registration/reset_password.html', {'uidb64': uidb64, 'token': token})



@login_required
def reset_password(request):
    email = request.user.email
    uid64 = urlsafe_base64_encode(force_bytes(request.user.pk))
    token = default_token_generator.make_token(request.user)
    link = request.build_absolute_uri(
        reverse("reseting_password", kwargs={"uidb64": uid64, "token": token})
    )

    send_mail(
        subject="Reset Password",
        message=f"Your're reset password link: {link}",
        from_email="sender@example.com",
        recipient_list=[email],
        fail_silently=False,
    )

    messages.success(request, "Reset password link sent")
    return redirect(reverse("profile", args=[request.user.username]))


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    num_comp = Company.objects.filter(user=user).count()
    num_accprop = (
        InvestmentProposal.objects.filter(investor=user).filter(status="PA").count()
    )
    num_rejprop = (
        InvestmentProposal.objects.filter(investor=user).filter(status="PR").count()
    )
    num_prop = InvestmentProposal.objects.filter(investor=user).count()
    notfs = reversed(Notifications.objects.filter(user=user))
    form = forms.ProfileForm(instance=user)
    return render(
        request,
        "registration/profile.html",
        {   
            "bool_notfs": bool(notfs),
            "notfs": notfs,
            "user": user,
            "num_comp": num_comp,
            "num_accprop": num_accprop,
            "num_rejprop": num_rejprop,
            "num_prop": num_prop,
            "form": form,
        },
    )


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
