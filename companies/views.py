from .forms import CompanyForm
from .models import Company as CompanyModel

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import Http404


def seeCompany(request, slug):
    try:
        company = get_object_or_404(CompanyModel, slug=slug)

    except Http404:
        messages.info(request, "Company can't be found")
        return redirect(reverse("showCompany"))

    if request.method == "POST":
        ...

    context = {"company": company}
    return render(request, "companies/see.html", context=context)


def showCompany(request):
    companies = CompanyModel.objects.all()

    if request.method == "POST":
        name = request.POST.get("company", None)

        if not name:
            messages.info(request, "Please, enter the company name")
            return redirect("/")

        companies = CompanyModel.objects.filter(name__icontains=name)

    context = {"companies": companies}
    return render(request, "companies/show.html", context=context)


@login_required
def addCompany(request):
    form = CompanyForm()

    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES)

        if form.is_valid() and form.is_multipart():
            instance = form.save(commit=False)
            instance.user = request.user

            instance.save()
            messages.success(request, "New company added successfully!")
            return redirect(reverse("showCompany"))

    context = {"form": form}
    return render(request, "companies/new.html", context=context)
