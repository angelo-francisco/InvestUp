from django.shortcuts import render
from .forms import CompanyForm


def addCompany(request):
    form = CompanyForm()

    if request.method == "POST":
        return

    context = {"form": form}
    return render(request, "companies/new.html", context=context)
